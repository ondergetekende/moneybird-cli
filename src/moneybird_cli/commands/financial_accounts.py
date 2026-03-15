"""Financial accounts commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "name", "type", "identifier", "currency", "active"]


@click.group(name="financial-accounts")
def financial_accounts() -> None:
    """Manage financial accounts (bank accounts, credit cards, etc.)."""


@financial_accounts.command("list")
@pass_context
def list_financial_accounts(ctx: Context) -> None:
    """List all financial accounts."""
    client = ctx.get_client()
    data = client.get("financial_accounts")
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)
