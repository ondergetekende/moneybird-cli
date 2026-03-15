"""Payments commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output


@click.group()
def payments() -> None:
    """View payments."""


@payments.command("get")
@click.argument("id")
@pass_context
def get_payment(ctx: Context, id: str) -> None:
    """Get a single payment by ID."""
    client = ctx.get_client()
    data = client.get(f"payments/{id}")
    echo_output(data, fmt=ctx.output_format)
