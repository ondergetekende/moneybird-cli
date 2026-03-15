"""Tests for the API client."""

from __future__ import annotations

import pytest
import responses

from moneybird_cli.client import MoneybirdApiError, MoneybirdClient

BASE = "https://moneybird.com/api/v2/123"


@pytest.fixture
def client():
    return MoneybirdClient(token="test-token", administration_id="123")


@responses.activate
def test_get_single(client):
    responses.add(
        responses.GET,
        f"{BASE}/contacts/1.json",
        json={"id": "1", "company_name": "Test"},
    )
    result = client.get("contacts/1")
    assert result["id"] == "1"
    assert "Bearer test-token" in responses.calls[0].request.headers["Authorization"]


@responses.activate
def test_get_all_pagination(client):
    # Page 1: full page
    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[{"id": str(i)} for i in range(100)],
    )
    # Page 2: partial page (end of results)
    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[{"id": str(i)} for i in range(100, 130)],
    )
    result = client.get_all("contacts")
    assert len(result) == 130
    assert len(responses.calls) == 2


@responses.activate
def test_get_all_single_page(client):
    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[{"id": "1"}, {"id": "2"}],
    )
    result = client.get_all("contacts")
    assert len(result) == 2
    assert len(responses.calls) == 1


@responses.activate
def test_post(client):
    responses.add(
        responses.POST,
        f"{BASE}/contacts.json",
        json={"id": "99", "company_name": "New"},
        status=201,
    )
    result = client.post("contacts", json={"contact": {"company_name": "New"}})
    assert result["id"] == "99"


@responses.activate
def test_patch(client):
    responses.add(
        responses.PATCH,
        f"{BASE}/contacts/1.json",
        json={"id": "1", "company_name": "Updated"},
    )
    result = client.patch("contacts/1", json={"contact": {"company_name": "Updated"}})
    assert result["company_name"] == "Updated"


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        f"{BASE}/contacts/1.json",
        status=204,
    )
    result = client.delete("contacts/1")
    assert result is None


@responses.activate
def test_error_handling(client):
    responses.add(
        responses.GET,
        f"{BASE}/contacts/999.json",
        json={"error": "Record not found"},
        status=404,
    )
    with pytest.raises(MoneybirdApiError) as exc_info:
        client.get("contacts/999")
    assert exc_info.value.status_code == 404


@responses.activate
def test_dry_run_skips_writes():
    client = MoneybirdClient(token="t", administration_id="123", dry_run=True)
    # No response registered - would fail if request was made
    result = client.post("contacts", json={"contact": {"company_name": "Test"}})
    assert result is None
    assert len(responses.calls) == 0


@responses.activate
def test_dry_run_allows_get():
    client = MoneybirdClient(token="t", administration_id="123", dry_run=True)
    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[],
    )
    result = client.get("contacts")
    assert result == []
