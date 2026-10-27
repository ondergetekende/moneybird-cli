"""Moneybird API client with pagination, rate limiting, and error handling."""

from __future__ import annotations

import logging
import time
from typing import Any

import click
import requests

logger = logging.getLogger(__name__)

API_BASE = "https://moneybird.com/api/v2"


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

    def _handle_response(self, response: requests.Response) -> tuple[Any, requests.Response]:
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "60"))
            logger.warning("Rate limited. Retrying after %d seconds.", retry_after)
            time.sleep(retry_after)
            return self._handle_response(
                self.session.send(response.request)  # type: ignore[arg-type]
            )

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
    ) -> Any:
        url = self._url(path)
        if self.verbose:
            click.echo(f"{method.upper()} {url}", err=True)
            if json:
                click.echo(f"  Body: {json}", err=True)

        if self.dry_run and method.upper() != "GET":
            click.echo(f"[dry-run] {method.upper()} {url}", err=True)
            return None

        response = self.session.request(method, url, params=params, json=json)
        data, _ = self._handle_response(response)
        return data

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
            reset = int(response.headers.get("RateLimit-Reset", "60"))
            if verbose:
                click.echo(f"Rate limit nearly exhausted, waiting {reset}s.", err=True)
            time.sleep(reset)

    def get(self, path: str, params: dict | None = None) -> Any:
        return self._request("GET", path, params=params)

    def download(self, path: str) -> bytes:
        """GET an endpoint that redirects (302) to a file and return its contents."""
        url = self._url(path)
        if self.verbose:
            click.echo(f"GET {url}", err=True)
        response = self.session.get(url, allow_redirects=False)
        if response.is_redirect:
            # Fetch without our session so the API token isn't sent to the file host.
            response = requests.get(response.headers["Location"])
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

    def post(self, path: str, json: dict | None = None) -> Any:
        return self._request("POST", path, json=json)

    def patch(self, path: str, json: dict | None = None) -> Any:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)
