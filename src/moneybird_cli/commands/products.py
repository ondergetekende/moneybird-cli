"""Products commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "title", "price", "currency", "tax_rate_id"]


@click.group()
def products() -> None:
    """Manage products."""


@products.command("list")
@click.option("--query", help="Filter by product name.")
@click.option("--page", type=int, default=None, help="Page number.")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_products(ctx: Context, query: str | None, page: int | None, per_page: int | None) -> None:
    """List all products."""
    client = ctx.get_client()
    params: dict = {}
    if query:
        params["query"] = query
    if page is not None:
        params["page"] = page
        if per_page:
            params["per_page"] = per_page
        data = client.get("products", params=params)
    else:
        data = client.get_all("products", params=params, per_page=per_page or 100)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@products.command("get")
@click.argument("id")
@pass_context
def get_product(ctx: Context, id: str) -> None:
    """Get a single product by ID."""
    client = ctx.get_client()
    data = client.get(f"products/{id}")
    echo_output(data, fmt=ctx.output_format)


@products.command("find")
@click.argument("identifier")
@pass_context
def find_product(ctx: Context, identifier: str) -> None:
    """Find a product by its identifier field."""
    client = ctx.get_client()
    data = client.get(f"products/identifier/{identifier}")
    echo_output(data, fmt=ctx.output_format)


@products.command("create")
@click.option("--title", required=True, help="Product title.")
@click.option("--description", help="Product description.")
@click.option("--price", help="Price (e.g., 29.95).")
@click.option("--currency", default="EUR", help="Currency code (default: EUR).")
@click.option("--tax-rate-id", help="Tax rate ID.")
@click.option("--ledger-account-id", help="Ledger account ID.")
@click.option("--identifier", help="Product identifier/SKU.")
@pass_context
def create_product(ctx: Context, **kwargs: str | None) -> None:
    """Create a new product."""
    client = ctx.get_client()
    product = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("products", json={"product": product})
    echo_output(data, fmt=ctx.output_format)


@products.command("update")
@click.argument("id")
@click.option("--title", help="Product title.")
@click.option("--description", help="Product description.")
@click.option("--price", help="Price.")
@click.option("--currency", help="Currency code.")
@click.option("--tax-rate-id", help="Tax rate ID.")
@click.option("--ledger-account-id", help="Ledger account ID.")
@click.option("--identifier", help="Product identifier/SKU.")
@pass_context
def update_product(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a product by ID."""
    client = ctx.get_client()
    product = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"products/{id}", json={"product": product})
    echo_output(data, fmt=ctx.output_format)


@products.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this product?")
@pass_context
def delete_product(ctx: Context, id: str) -> None:
    """Delete a product by ID."""
    client = ctx.get_client()
    client.delete(f"products/{id}")
    if not ctx.quiet:
        click.echo(f"Product {id} deleted.")
