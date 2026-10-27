"""Ledger accounts commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "name", "account_type", "account_id"]
ACCOUNT_TYPES = [
    "non_current_assets",
    "current_assets",
    "equity",
    "provisions",
    "non_current_liabilities",
    "current_liabilities",
    "revenue",
    "direct_costs",
    "expenses",
    "other_income_expenses",
]


@click.group(name="ledger-accounts")
def ledger_accounts() -> None:
    """Manage ledger accounts."""


@ledger_accounts.command("list")
@pass_context
def list_ledger_accounts(ctx: Context) -> None:
    """List all ledger accounts."""
    client = ctx.get_client()
    data = client.get("ledger_accounts")
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@ledger_accounts.command("get")
@click.argument("id")
@pass_context
def get_ledger_account(ctx: Context, id: str) -> None:
    """Get a single ledger account by ID."""
    client = ctx.get_client()
    data = client.get(f"ledger_accounts/{id}")
    echo_output(data, fmt=ctx.output_format)


@ledger_accounts.command("create")
@click.option("--name", required=True, help="Account name.")
@click.option("--account-type", required=True, type=click.Choice(ACCOUNT_TYPES), help="Account type.")
@click.option("--rgs-code", required=True, help="RGS 3.5 code (e.g., WMfoBelMfo).")
@click.option("--parent-id", help="Parent ledger account ID.")
@pass_context
def create_ledger_account(ctx: Context, rgs_code: str, **kwargs: str | None) -> None:
    """Create a new ledger account."""
    client = ctx.get_client()
    account = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("ledger_accounts", json={"ledger_account": account, "rgs_code": rgs_code})
    echo_output(data, fmt=ctx.output_format)


@ledger_accounts.command("update")
@click.argument("id")
@click.option("--name", help="Account name.")
@click.option("--account-type", type=click.Choice(ACCOUNT_TYPES), help="Account type.")
@pass_context
def update_ledger_account(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a ledger account by ID."""
    client = ctx.get_client()
    account = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"ledger_accounts/{id}", json={"ledger_account": account})
    echo_output(data, fmt=ctx.output_format)


@ledger_accounts.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this ledger account?")
@pass_context
def delete_ledger_account(ctx: Context, id: str) -> None:
    """Delete a ledger account by ID."""
    client = ctx.get_client()
    client.delete(f"ledger_accounts/{id}")
    if not ctx.quiet:
        click.echo(f"Ledger account {id} deleted.")
