"""Financial statements commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output


@click.group(name="financial-statements")
def financial_statements() -> None:
    """Manage financial statements."""


@financial_statements.command("create")
@click.option("--financial-account-id", required=True, help="Financial account ID.")
@click.option("--reference", required=True, help="Statement reference.")
@click.option("--official-date", help="Official date (YYYY-MM-DD).")
@click.option("--official-balance", help="Official closing balance.")
@pass_context
def create_financial_statement(ctx: Context, **kwargs: str | None) -> None:
    """Create a new financial statement."""
    client = ctx.get_client()
    statement = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("financial_statements", json={"financial_statement": statement})
    echo_output(data, fmt=ctx.output_format)


@financial_statements.command("update")
@click.argument("id")
@click.option("--reference", help="Statement reference.")
@click.option("--official-date", help="Official date (YYYY-MM-DD).")
@click.option("--official-balance", help="Official closing balance.")
@pass_context
def update_financial_statement(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a financial statement by ID."""
    client = ctx.get_client()
    statement = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"financial_statements/{id}", json={"financial_statement": statement})
    echo_output(data, fmt=ctx.output_format)


@financial_statements.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this financial statement?")
@pass_context
def delete_financial_statement(ctx: Context, id: str) -> None:
    """Delete a financial statement by ID."""
    client = ctx.get_client()
    client.delete(f"financial_statements/{id}")
    if not ctx.quiet:
        click.echo(f"Financial statement {id} deleted.")
