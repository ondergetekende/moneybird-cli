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
def test_get_all_respects_rate_limit(client, monkeypatch):
    """When RateLimit-Remaining hits 1, get_all pauses before the next request."""
    slept = []
    monkeypatch.setattr("moneybird_cli.client.time.sleep", lambda s: slept.append(s))

    # Page 1: full page, rate limit nearly exhausted
    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[{"id": str(i)} for i in range(100)],
        headers={"RateLimit-Remaining": "1", "RateLimit-Reset": "5"},
    )
    # Page 2: partial page
    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[{"id": "100"}],
    )
    result = client.get_all("contacts")
    assert len(result) == 101
    assert slept == [5]


@responses.activate
def test_get_all_no_pause_when_remaining_high(client, monkeypatch):
    slept = []
    monkeypatch.setattr("moneybird_cli.client.time.sleep", lambda s: slept.append(s))

    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[{"id": str(i)} for i in range(100)],
        headers={"RateLimit-Remaining": "50", "RateLimit-Reset": "300"},
    )
    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[{"id": "100"}],
    )
    result = client.get_all("contacts")
    assert len(result) == 101
    assert slept == []


@responses.activate
def test_timezone_header_sent():
    client = MoneybirdClient(token="t", administration_id="123", timezone="Europe/Amsterdam")
    responses.add(responses.GET, f"{BASE}/contacts.json", json=[])
    client.get("contacts")
    assert responses.calls[0].request.headers["Time-Zone"] == "Europe/Amsterdam"


@responses.activate
def test_no_timezone_header_when_not_set():
    client = MoneybirdClient(token="t", administration_id="123")
    responses.add(responses.GET, f"{BASE}/contacts.json", json=[])
    client.get("contacts")
    assert "Time-Zone" not in responses.calls[0].request.headers


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


@responses.activate
def test_upload_sends_multipart(client, tmp_path):
    responses.add(responses.POST, f"{BASE}/sales_invoices/1/attachments.json", json={})
    f = tmp_path / "a.pdf"
    f.write_bytes(b"%PDF")
    client.upload("sales_invoices/1/attachments", str(f))
    request = responses.calls[0].request
    assert request.headers["Content-Type"].startswith("multipart/form-data; boundary=")
    assert b"%PDF" in request.body


@responses.activate
def test_bool_query_params_are_lowercase(client):
    responses.add(responses.GET, f"{BASE}/users.json", json=[])
    client.get("users", params={"include_inactive": True})
    assert responses.calls[0].request.url.endswith("include_inactive=true")
