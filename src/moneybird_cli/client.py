"""Moneybird API client with pagination, rate limiting, and error handling."""

from __future__ import annotations

import logging
import math
import time
from datetime import timezone
from email.utils import parsedate_to_datetime
from typing import Any

import click
import requests

logger = logging.getLogger(__name__)

API_BASE = "https://moneybird.com/api/v2"


def _rate_limit_delay(value: str | None) -> int:
    if value is None:
        return 60
    try:
        seconds = int(value)
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            timestamp = date.timestamp()
        except (TypeError, ValueError, OverflowError):
            return 60
    else:
        if seconds < 0:
            return 60
        if seconds < 1_000_000_000:
            return seconds
        timestamp = seconds
    return max(0, math.ceil(timestamp - time.time()))


class MoneybirdApiError(click.ClickException):
    """API error with HTTP status code context."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"API error {status_code}: {message}")


class MoneybirdClient:
    """HTTP client for the Moneybird API."""

    def __init__(
        self,
        token: str,
        administration_id: str,
        dry_run: bool = False,
        verbose: bool = False,
        timezone: str | None = None,
    ) -> None:
        self.token = token
        self.administration_id = administration_id
        self.dry_run = dry_run
        self.verbose = verbose
        self.base_url = f"{API_BASE}/{administration_id}"
        self.session = requests.Session()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if timezone:
            headers["Time-Zone"] = timezone
        self.session.headers.update(headers)

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path}.json"

    def _retry_rate_limited(
        self, response: requests.Response, allow_redirects: bool = True
    ) -> requests.Response:
        while response.status_code == 429:
            retry_after = _rate_limit_delay(response.headers.get("Retry-After"))
            logger.warning("Rate limited. Retrying after %d seconds.", retry_after)
            time.sleep(retry_after)
            response = self.session.send(
                response.request, allow_redirects=allow_redirects  # type: ignore[arg-type]
            )
        return response

    def _handle_response(self, response: requests.Response) -> tuple[Any, requests.Response]:
        response = self._retry_rate_limited(response)

        if response.status_code == 204:
            return None, response

        if response.status_code >= 400:
            try:
                body = response.json()
                message = body.get("error", body.get("message", response.text))
            except (ValueError, KeyError):
                message = response.text
            raise MoneybirdApiError(response.status_code, message)

        if not response.content:
            return None, response
        return response.json(), response

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json: dict | None = None,
        files: dict | None = None,
        data: dict | None = None,
    ) -> Any:
        url = self._url(path)
        if params:
            params = {k: str(v).lower() if isinstance(v, bool) else v for k, v in params.items()}
        if self.verbose:
            click.echo(f"{method.upper()} {url}", err=True)
            if json:
                click.echo(f"  Body: {json}", err=True)

        if self.dry_run and method.upper() != "GET":
            click.echo(f"[dry-run] {method.upper()} {url}", err=True)
            return None

        # Content-Type None lets requests set the multipart boundary for uploads.
        headers = {"Content-Type": None} if files else None
        response = self.session.request(
            method, url, params=params, json=json, files=files, data=data, headers=headers
        )
        result, _ = self._handle_response(response)
        return result

    def _request_with_headers(
        self,
        method: str,
        path: str,
        params: dict | None = None,
    ) -> tuple[Any, requests.Response]:
        """Like _request, but also returns the response for header inspection."""
        url = self._url(path)
        if self.verbose:
            click.echo(f"{method.upper()} {url}", err=True)

        response = self.session.request(method, url, params=params)
        return self._handle_response(response)

    @staticmethod
    def _respect_rate_limit(response: requests.Response, verbose: bool = False) -> None:
        """Sleep if rate limit is nearly exhausted."""
        remaining = response.headers.get("RateLimit-Remaining")
        if remaining is not None and int(remaining) <= 1:
            reset = _rate_limit_delay(response.headers.get("RateLimit-Reset"))
            if verbose:
                click.echo(f"Rate limit nearly exhausted, waiting {reset}s.", err=True)
            time.sleep(reset)

    def get(self, path: str, params: dict | None = None) -> Any:
        return self._request("GET", path, params=params)

    def download(self, path: str, method: str = "GET") -> bytes:
        """Fetch a file, following a 302 redirect if the API returns one."""
        url = self._url(path)
        if self.verbose:
            click.echo(f"{method} {url}", err=True)
        response = self._retry_rate_limited(
            self.session.request(method, url, allow_redirects=False), allow_redirects=False
        )
        if response.is_redirect:
            # Fetch without our session so the API token isn't sent to the file host.
            response = self._retry_rate_limited(requests.get(response.headers["Location"]))
        if response.status_code >= 400:
            self._handle_response(response)
        return response.content

    @staticmethod
    def list_administrations(token: str) -> list[dict]:
        """List all administrations accessible with the given token."""
        url = f"{API_BASE}/administrations.json"
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        if response.status_code >= 400:
            try:
                body = response.json()
                message = body.get("error", body.get("message", response.text))
            except (ValueError, KeyError):
                message = response.text
            raise MoneybirdApiError(response.status_code, message)
        return response.json()

    def get_all(
        self, path: str, params: dict | None = None, per_page: int = 100
    ) -> list[dict]:
        """GET with automatic pagination. Returns all results.

        Respects rate limit headers: pauses when RateLimit-Remaining is low.
        """
        params = dict(params or {})
        params["per_page"] = per_page
        page = 1
        results: list[dict] = []
        while True:
            params["page"] = page
            data, response = self._request_with_headers("GET", path, params=params)
            if not data:
                break
            results.extend(data)
            if len(data) < per_page:
                break
            self._respect_rate_limit(response, verbose=self.verbose)
            page += 1
        return results

    def post(self, path: str, json: dict | None = None, params: dict | None = None) -> Any:
        return self._request("POST", path, params=params, json=json)

    def upload(self, path: str, file_path: str, data: dict | None = None) -> Any:
        """POST a file as multipart/form-data (field name `file`)."""
        with open(file_path, "rb") as f:
            return self._request("POST", path, files={"file": f}, data=data)

    def sync_all(self, path: str, params: dict | None = None) -> list[dict]:
        """Fetch every record via the synchronization API: ids first, then records in batches of 100."""
        url = self._url(f"{path}/synchronization")
        ids = [r["id"] for r in self.get(f"{path}/synchronization", params=params) or []]
        results: list[dict] = []
        for i in range(0, len(ids), 100):
            # Direct session call: this POST is a read, so it must also run in dry-run mode.
            data, _ = self._handle_response(self.session.post(url, json={"ids": ids[i:i + 100]}))
            results += data or []
        return results

    def patch(self, path: str, json: dict | None = None) -> Any:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)
