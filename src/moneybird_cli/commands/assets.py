"""Assets commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "name", "purchase_date", "purchase_value", "current_value"]


@click.group()
def assets() -> None:
    """Manage assets (company cars, laptops, furniture, etc.)."""


@assets.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_assets(ctx: Context, fetch_all: bool, page: int | None, per_page: int | None) -> None:
    """List assets. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    if fetch_all:
        data = client.get_all("assets", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("assets", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@assets.command("get")
@click.argument("id")
@pass_context
def get_asset(ctx: Context, id: str) -> None:
    """Get a single asset by ID."""
    client = ctx.get_client()
    data = client.get(f"assets/{id}")
    echo_output(data, fmt=ctx.output_format)


@assets.command("create")
@click.option("--name", required=True, help="Asset name.")
@click.option("--purchase-date", help="Purchase date (YYYY-MM-DD).")
@click.option("--purchase-value", help="Purchase value.")
@pass_context
def create_asset(ctx: Context, **kwargs: str | None) -> None:
    """Create a new asset."""
    client = ctx.get_client()
    asset = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("assets", json={"asset": asset})
    echo_output(data, fmt=ctx.output_format)


@assets.command("update")
@click.argument("id")
@click.option("--name", help="Asset name.")
@pass_context
def update_asset(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update an asset by ID."""
    client = ctx.get_client()
    asset = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"assets/{id}", json={"asset": asset})
    echo_output(data, fmt=ctx.output_format)


@assets.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this asset?")
@pass_context
def delete_asset(ctx: Context, id: str) -> None:
    """Delete an asset by ID."""
    client = ctx.get_client()
    client.delete(f"assets/{id}")
    if not ctx.quiet:
        click.echo(f"Asset {id} deleted.")
