"""Tests for sales invoices commands."""

import responses

BASE = "https://moneybird.com/api/v2/123456"


@responses.activate
def test_list_invoices(logged_in_runner):
    responses.add(
        responses.GET,
        f"{BASE}/sales_invoices.json",
        json=[
            {
                "id": "1",
                "invoice_id": "2024-001",
                "contact_id": "10",
                "state": "open",
                "invoice_date": "2024-01-01",
                "due_date": "2024-02-01",
                "total_price_incl_tax": "121.00",
                "total_unpaid": "121.00",
            },
        ],
    )
    result = logged_in_runner("sales-invoices", "list")
    assert result.exit_code == 0
    assert "2024-001" in result.output


@responses.activate
def test_get_invoice(logged_in_runner):
    responses.add(
        responses.GET,
        f"{BASE}/sales_invoices/1.json",
        json={"id": "1", "invoice_id": "2024-001", "state": "open"},
    )
    result = logged_in_runner("sales-invoices", "get", "1")
    assert result.exit_code == 0
    assert "2024-001" in result.output


@responses.activate
def test_create_invoice(logged_in_runner):
    responses.add(
        responses.POST,
        f"{BASE}/sales_invoices.json",
        json={"id": "99", "invoice_id": "2024-099"},
        status=201,
    )
    result = logged_in_runner("sales-invoices", "create", "--contact-id", "10")
    assert result.exit_code == 0


@responses.activate
def test_delete_invoice(logged_in_runner):
    responses.add(
        responses.DELETE,
        f"{BASE}/sales_invoices/1.json",
        status=204,
    )
    result = logged_in_runner("sales-invoices", "delete", "--yes", "1")
    assert result.exit_code == 0
    assert "deleted" in result.output


@responses.activate
def test_send_invoice(logged_in_runner):
    responses.add(
        responses.PATCH,
        f"{BASE}/sales_invoices/1/sends_an_invoice.json",
        json={"id": "1", "state": "open"},
    )
    result = logged_in_runner("sales-invoices", "send", "1")
    assert result.exit_code == 0


@responses.activate
def test_pay_invoice(logged_in_runner):
    responses.add(
        responses.PATCH,
        f"{BASE}/sales_invoices/1/register_a_payment.json",
        json={"id": "1", "state": "paid"},
    )
    result = logged_in_runner(
        "sales-invoices", "pay", "1", "--amount", "121.00", "--date", "2024-01-15"
    )
    assert result.exit_code == 0


@responses.activate
def test_credit_invoice(logged_in_runner):
    responses.add(
        responses.PATCH,
        f"{BASE}/sales_invoices/1/duplicate_creditinvoice.json",
        json={"id": "2", "invoice_id": "2024-002"},
    )
    result = logged_in_runner("sales-invoices", "credit", "1")
    assert result.exit_code == 0
