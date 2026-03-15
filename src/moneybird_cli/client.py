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
    ) -> None:
        self.token = token
        self.administration_id = administration_id
        self.dry_run = dry_run
        self.verbose = verbose
        self.base_url = f"{API_BASE}/{administration_id}"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path}.json"

    def _handle_response(self, response: requests.Response) -> Any:
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "60"))
            logger.warning("Rate limited. Retrying after %d seconds.", retry_after)
            time.sleep(retry_after)
            # Retry the same request
            return self._handle_response(
                self.session.send(response.request)  # type: ignore[arg-type]
            )

        if response.status_code == 204:
            return None

        if response.status_code >= 400:
            try:
                body = response.json()
                message = body.get("error", body.get("message", response.text))
            except (ValueError, KeyError):
                message = response.text
            raise MoneybirdApiError(response.status_code, message)

        if not response.content:
            return None
        return response.json()

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
        return self._handle_response(response)

    def get(self, path: str, params: dict | None = None) -> Any:
        return self._request("GET", path, params=params)

    def get_all(
        self, path: str, params: dict | None = None, per_page: int = 100
    ) -> list[dict]:
        """GET with automatic pagination. Returns all results."""
        params = dict(params or {})
        params["per_page"] = per_page
        page = 1
        results: list[dict] = []
        while True:
            params["page"] = page
            data = self._request("GET", path, params=params)
            if not data:
                break
            results.extend(data)
            if len(data) < per_page:
                break
            page += 1
        return results

    def post(self, path: str, json: dict | None = None) -> Any:
        return self._request("POST", path, json=json)

    def patch(self, path: str, json: dict | None = None) -> Any:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)
