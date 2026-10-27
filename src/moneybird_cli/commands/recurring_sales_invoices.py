"""Recurring sales invoices commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output
from moneybird_cli.commands._common import add_notes, add_sync

LIST_COLUMNS = ["id", "contact_id", "frequency_type", "frequency", "start_date", "last_date", "active"]


@click.group(name="recurring-sales-invoices")
def recurring_sales_invoices() -> None:
    """Manage recurring sales invoices."""


@recurring_sales_invoices.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_recurring(ctx: Context, fetch_all: bool, page: int | None, per_page: int | None) -> None:
    """List recurring sales invoices. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    if fetch_all:
        data = client.get_all("recurring_sales_invoices", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("recurring_sales_invoices", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@recurring_sales_invoices.command("get")
@click.argument("id")
@pass_context
def get_recurring(ctx: Context, id: str) -> None:
    """Get a single recurring sales invoice by ID."""
    client = ctx.get_client()
    data = client.get(f"recurring_sales_invoices/{id}")
    echo_output(data, fmt=ctx.output_format)


@recurring_sales_invoices.command("create")
@click.option("--contact-id", required=True, help="Contact ID.")
@click.option("--frequency-type", required=True, type=click.Choice(["day", "week", "month", "quarter", "year"]), help="Frequency type.")
@click.option("--frequency", required=True, type=int, help="Frequency interval (e.g., 1 for every month).")
@click.option("--invoice-date", help="Date of the first invoice (YYYY-MM-DD).")
@click.option("--first-due-interval", type=int, help="Days until each invoice is due.")
@click.option("--workflow-id", help="Workflow ID.")
@click.option("--document-style-id", help="Document style ID.")
@click.option("--currency", help="Currency code (default: EUR).")
@pass_context
def create_recurring(ctx: Context, **kwargs: str | int | None) -> None:
    """Create a new recurring sales invoice."""
    client = ctx.get_client()
    invoice = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("recurring_sales_invoices", json={"recurring_sales_invoice": invoice})
    echo_output(data, fmt=ctx.output_format)


@recurring_sales_invoices.command("update")
@click.argument("id")
@click.option("--contact-id", help="Contact ID.")
@click.option("--frequency-type", type=click.Choice(["day", "week", "month", "quarter", "year"]), help="Frequency type.")
@click.option("--frequency", type=int, help="Frequency interval.")
@click.option("--invoice-date", help="Date of the next invoice (YYYY-MM-DD).")
@click.option("--currency", help="Currency code.")
@pass_context
def update_recurring(ctx: Context, id: str, **kwargs: str | int | None) -> None:
    """Update a recurring sales invoice by ID."""
    client = ctx.get_client()
    invoice = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"recurring_sales_invoices/{id}", json={"recurring_sales_invoice": invoice})
    echo_output(data, fmt=ctx.output_format)


@recurring_sales_invoices.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this recurring invoice?")
@pass_context
def delete_recurring(ctx: Context, id: str) -> None:
    """Delete a recurring sales invoice by ID."""
    client = ctx.get_client()
    client.delete(f"recurring_sales_invoices/{id}")
    if not ctx.quiet:
        click.echo(f"Recurring sales invoice {id} deleted.")


add_sync(recurring_sales_invoices, "recurring_sales_invoices", LIST_COLUMNS)
add_notes(recurring_sales_invoices, "recurring_sales_invoices")
