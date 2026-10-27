"""Sales invoices commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = [
    "id",
    "invoice_id",
    "contact_id",
    "state",
    "invoice_date",
    "due_date",
    "total_price_incl_tax",
    "total_unpaid",
]


@click.group(name="sales-invoices")
def sales_invoices() -> None:
    """Manage sales invoices."""


@sales_invoices.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--state", help="Filter by state (draft, open, scheduled, pending_payment, reminded, late, paid, uncollectible).")
@click.option("--period", help="Filter by period (e.g., this_month, prev_year, 202401..202412).")
@click.option("--contact-id", help="Filter by contact ID.")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_invoices(
    ctx: Context,
    fetch_all: bool,
    state: str | None,
    period: str | None,
    contact_id: str | None,
    page: int | None,
    per_page: int | None,
) -> None:
    """List sales invoices. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    filters = []
    if state:
        filters.append(f"state:{state}")
    if period:
        filters.append(f"period:{period}")
    if contact_id:
        filters.append(f"contact_id:{contact_id}")
    if filters:
        params["filter"] = ",".join(filters)
    if fetch_all:
        data = client.get_all("sales_invoices", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("sales_invoices", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@sales_invoices.command("get")
@click.argument("id")
@pass_context
def get_invoice(ctx: Context, id: str) -> None:
    """Get a single sales invoice by ID."""
    client = ctx.get_client()
    data = client.get(f"sales_invoices/{id}")
    echo_output(data, fmt=ctx.output_format)


@sales_invoices.command("find")
@click.argument("invoice_id")
@pass_context
def find_invoice(ctx: Context, invoice_id: str) -> None:
    """Find a sales invoice by its invoice ID."""
    client = ctx.get_client()
    data = client.get(f"sales_invoices/find_by_invoice_id/{invoice_id}")
    echo_output(data, fmt=ctx.output_format)


@sales_invoices.command("create")
@click.option("--contact-id", required=True, help="Contact ID.")
@click.option("--invoice-date", help="Invoice date (YYYY-MM-DD).")
@click.option("--first-due-interval", type=int, help="Days until the invoice is due.")
@click.option("--reference", help="Custom reference.")
@click.option("--currency", default="EUR", help="Currency code (default: EUR).")
@click.option("--discount", help="Discount percentage.")
@click.option("--workflow-id", help="Workflow ID.")
@click.option("--document-style-id", help="Document style ID.")
@pass_context
def create_invoice(ctx: Context, **kwargs: str | None) -> None:
    """Create a new sales invoice.

    Use 'sales-invoices add-line' to add detail lines after creation.
    """
    client = ctx.get_client()
    invoice = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("sales_invoices", json={"sales_invoice": invoice})
    echo_output(data, fmt=ctx.output_format)


@sales_invoices.command("update")
@click.argument("id")
@click.option("--contact-id", help="Contact ID.")
@click.option("--invoice-date", help="Invoice date (YYYY-MM-DD).")
@click.option("--first-due-interval", type=int, help="Days until the invoice is due.")
@click.option("--reference", help="Custom reference.")
@click.option("--discount", help="Discount percentage.")
@pass_context
def update_invoice(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a sales invoice by ID."""
    client = ctx.get_client()
    invoice = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"sales_invoices/{id}", json={"sales_invoice": invoice})
    echo_output(data, fmt=ctx.output_format)


@sales_invoices.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this invoice?")
@pass_context
def delete_invoice(ctx: Context, id: str) -> None:
    """Delete a sales invoice by ID."""
    client = ctx.get_client()
    client.delete(f"sales_invoices/{id}")
    if not ctx.quiet:
        click.echo(f"Sales invoice {id} deleted.")


@sales_invoices.command("send")
@click.argument("id")
@click.option("--delivery-method", type=click.Choice(["Email", "Peppol", "Manual"]), default="Email", help="Delivery method.")
@click.option("--email-address", help="Override recipient email.")
@click.option("--email-message", help="Custom email message.")
@pass_context
def send_invoice(ctx: Context, id: str, delivery_method: str, email_address: str | None, email_message: str | None) -> None:
    """Send a sales invoice."""
    client = ctx.get_client()
    body: dict = {"delivery_method": delivery_method}
    if email_address:
        body["email_address"] = email_address
    if email_message:
        body["email_message"] = email_message
    data = client.patch(f"sales_invoices/{id}/send_invoice", json={"sales_invoice_sending": body})
    echo_output(data, fmt=ctx.output_format)


@sales_invoices.command("pay")
@click.argument("id")
@click.option("--amount", required=True, help="Payment amount.")
@click.option("--date", "payment_date", required=True, help="Payment date (YYYY-MM-DD).")
@click.option("--financial-account-id", help="Financial account ID.")
@pass_context
def pay_invoice(ctx: Context, id: str, amount: str, payment_date: str, financial_account_id: str | None) -> None:
    """Register a payment for a sales invoice."""
    client = ctx.get_client()
    payment: dict = {
        "payment_date": payment_date,
        "price": amount,
    }
    if financial_account_id:
        payment["financial_account_id"] = financial_account_id
    data = client.patch(f"sales_invoices/{id}/register_payment", json={"payment": payment})
    echo_output(data, fmt=ctx.output_format)


@sales_invoices.command("pdf")
@click.argument("id")
@click.option("--output", "output_path", type=click.Path(), default=None, help="Output file path.")
@pass_context
def download_pdf(ctx: Context, id: str, output_path: str | None) -> None:
    """Download a sales invoice as PDF."""
    client = ctx.get_client()
    content = client.download(f"sales_invoices/{id}/download_pdf")
    path = output_path or f"invoice-{id}.pdf"
    with open(path, "wb") as f:
        f.write(content)
    if not ctx.quiet:
        click.echo(f"PDF saved to {path}")


@sales_invoices.command("credit")
@click.argument("id")
@pass_context
def credit_invoice(ctx: Context, id: str) -> None:
    """Create a credit invoice from a sales invoice."""
    client = ctx.get_client()
    data = client.patch(f"sales_invoices/{id}/duplicate_creditinvoice")
    echo_output(data, fmt=ctx.output_format)
