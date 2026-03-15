"""Tax rates commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "name", "percentage", "tax_rate_type", "active"]


@click.group(name="tax-rates")
def tax_rates() -> None:
    """View tax rates."""


@tax_rates.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_tax_rates(ctx: Context, fetch_all: bool, page: int | None, per_page: int | None) -> None:
    """List tax rates. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    if fetch_all:
        data = client.get_all("tax_rates", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("tax_rates", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)
