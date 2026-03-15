"""Purchase transactions commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "state", "amount", "date", "description", "sepa_iban"]


@click.group(name="purchase-transactions")
def purchase_transactions() -> None:
    """Manage purchase transactions."""


@purchase_transactions.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--state", type=click.Choice(["all", "open", "pending_payment", "paid", "cancelled"]), default=None, help="Filter by state.")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_purchase_transactions(ctx: Context, fetch_all: bool, state: str | None, page: int | None, per_page: int | None) -> None:
    """List purchase transactions. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    if state:
        params["filter"] = f"state:{state}"
    if fetch_all:
        data = client.get_all("purchase_transactions", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("purchase_transactions", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@purchase_transactions.command("get")
@click.argument("id")
@pass_context
def get_purchase_transaction(ctx: Context, id: str) -> None:
    """Get a single purchase transaction by ID."""
    client = ctx.get_client()
    data = client.get(f"purchase_transactions/{id}")
    echo_output(data, fmt=ctx.output_format)


@purchase_transactions.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this purchase transaction?")
@pass_context
def delete_purchase_transaction(ctx: Context, id: str) -> None:
    """Delete a pending purchase transaction by ID."""
    client = ctx.get_client()
    client.delete(f"purchase_transactions/{id}")
    if not ctx.quiet:
        click.echo(f"Purchase transaction {id} deleted.")
