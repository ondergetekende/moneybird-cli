"""Tests for contacts commands."""

import responses

BASE = "https://moneybird.com/api/v2/123456"


@responses.activate
def test_list_contacts(logged_in_runner):
    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[
            {"id": "1", "company_name": "Acme", "firstname": "", "lastname": "", "email": ""},
        ],
    )
    result = logged_in_runner("contacts", "list")
    assert result.exit_code == 0
    assert "Acme" in result.output


@responses.activate
def test_get_contact(logged_in_runner):
    responses.add(
        responses.GET,
        f"{BASE}/contacts/1.json",
        json={"id": "1", "company_name": "Acme", "email": "info@acme.com"},
    )
    result = logged_in_runner("contacts", "get", "1")
    assert result.exit_code == 0
    assert "Acme" in result.output


@responses.activate
def test_create_contact(logged_in_runner):
    responses.add(
        responses.POST,
        f"{BASE}/contacts.json",
        json={"id": "99", "company_name": "NewCo"},
        status=201,
    )
    result = logged_in_runner("contacts", "create", "--company-name", "NewCo")
    assert result.exit_code == 0
    body = responses.calls[0].request.body
    assert b"NewCo" in body


@responses.activate
def test_delete_contact(logged_in_runner):
    responses.add(
        responses.DELETE,
        f"{BASE}/contacts/1.json",
        status=204,
    )
    result = logged_in_runner("contacts", "delete", "--yes", "1")
    assert result.exit_code == 0
    assert "deleted" in result.output


@responses.activate
def test_search_contacts(logged_in_runner):
    responses.add(
        responses.GET,
        f"{BASE}/contacts.json",
        json=[
            {"id": "1", "company_name": "Acme", "firstname": "", "lastname": "", "email": ""},
        ],
    )
    result = logged_in_runner("contacts", "search", "Acme")
    assert result.exit_code == 0
    assert "Acme" in result.output


@responses.activate
def test_archive_contact(logged_in_runner):
    responses.add(
        responses.PATCH,
        f"{BASE}/contacts/1/archive.json",
        json={},
    )
    result = logged_in_runner("contacts", "archive", "1")
    assert result.exit_code == 0
    assert "archived" in result.output
