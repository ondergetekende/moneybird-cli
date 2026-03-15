"""Ledger accounts commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "name", "account_type", "account_id"]


@click.group(name="ledger-accounts")
def ledger_accounts() -> None:
    """Manage ledger accounts."""


@ledger_accounts.command("list")
@click.option("--page", type=int, default=None, help="Page number.")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_ledger_accounts(ctx: Context, page: int | None, per_page: int | None) -> None:
    """List all ledger accounts."""
    client = ctx.get_client()
    params: dict = {}
    if page is not None:
        params["page"] = page
        if per_page:
            params["per_page"] = per_page
        data = client.get("ledger_accounts", params=params)
    else:
        data = client.get_all("ledger_accounts", params=params, per_page=per_page or 100)
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
@click.option("--account-type", required=True, help="Account type.")
@click.option("--parent-id", help="Parent ledger account ID.")
@pass_context
def create_ledger_account(ctx: Context, **kwargs: str | None) -> None:
    """Create a new ledger account."""
    client = ctx.get_client()
    account = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("ledger_accounts", json={"ledger_account": account})
    echo_output(data, fmt=ctx.output_format)


@ledger_accounts.command("update")
@click.argument("id")
@click.option("--name", help="Account name.")
@click.option("--account-type", help="Account type.")
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
