"""Financial mutations commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "date", "amount", "code", "message", "contra_account_name"]


@click.group(name="financial-mutations")
def financial_mutations() -> None:
    """Manage financial mutations (bank transactions)."""


@financial_mutations.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_financial_mutations(ctx: Context, fetch_all: bool, page: int | None, per_page: int | None) -> None:
    """List financial mutations. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    if fetch_all:
        data = client.get_all("financial_mutations", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("financial_mutations", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@financial_mutations.command("get")
@click.argument("id")
@pass_context
def get_financial_mutation(ctx: Context, id: str) -> None:
    """Get a single financial mutation by ID."""
    client = ctx.get_client()
    data = client.get(f"financial_mutations/{id}")
    echo_output(data, fmt=ctx.output_format)


@financial_mutations.command("link")
@click.argument("id")
@click.option("--booking-type", required=True, help="Booking type (e.g., SalesInvoice, Document, LedgerAccount).")
@click.option("--booking-id", required=True, help="Booking ID.")
@click.option("--price", help="Amount to link.")
@click.option("--description", help="Description.")
@pass_context
def link_booking(ctx: Context, id: str, booking_type: str, booking_id: str, price: str | None, description: str | None) -> None:
    """Link a financial mutation to a booking."""
    client = ctx.get_client()
    body: dict = {"booking_type": booking_type, "booking_id": booking_id}
    if price:
        body["price_base"] = price
    if description:
        body["description"] = description
    data = client.patch(f"financial_mutations/{id}/link_booking", json=body)
    echo_output(data, fmt=ctx.output_format)


@financial_mutations.command("unlink")
@click.argument("id")
@click.option("--booking-type", required=True, help="Booking type (Payment or LedgerAccountBooking).")
@click.option("--booking-id", required=True, help="Booking ID.")
@pass_context
def unlink_booking(ctx: Context, id: str, booking_type: str, booking_id: str) -> None:
    """Unlink a booking from a financial mutation."""
    client = ctx.get_client()
    data = client.delete(f"financial_mutations/{id}/unlink_booking")
    echo_output(data, fmt=ctx.output_format)
