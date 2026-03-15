"""Estimates commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = [
    "id",
    "estimate_id",
    "contact_id",
    "state",
    "estimate_date",
    "total_price_incl_tax",
]


@click.group()
def estimates() -> None:
    """Manage estimates."""


@estimates.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_estimates(ctx: Context, fetch_all: bool, page: int | None, per_page: int | None) -> None:
    """List estimates. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    if fetch_all:
        data = client.get_all("estimates", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("estimates", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@estimates.command("get")
@click.argument("id")
@pass_context
def get_estimate(ctx: Context, id: str) -> None:
    """Get a single estimate by ID."""
    client = ctx.get_client()
    data = client.get(f"estimates/{id}")
    echo_output(data, fmt=ctx.output_format)


@estimates.command("create")
@click.option("--contact-id", required=True, help="Contact ID.")
@click.option("--estimate-date", help="Estimate date (YYYY-MM-DD).")
@click.option("--due-date", help="Due date (YYYY-MM-DD).")
@click.option("--reference", help="Custom reference.")
@click.option("--currency", default="EUR", help="Currency code (default: EUR).")
@click.option("--discount", help="Discount percentage.")
@click.option("--workflow-id", help="Workflow ID.")
@click.option("--document-style-id", help="Document style ID.")
@pass_context
def create_estimate(ctx: Context, **kwargs: str | None) -> None:
    """Create a new estimate."""
    client = ctx.get_client()
    estimate = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("estimates", json={"estimate": estimate})
    echo_output(data, fmt=ctx.output_format)


@estimates.command("update")
@click.argument("id")
@click.option("--contact-id", help="Contact ID.")
@click.option("--estimate-date", help="Estimate date (YYYY-MM-DD).")
@click.option("--due-date", help="Due date (YYYY-MM-DD).")
@click.option("--reference", help="Custom reference.")
@click.option("--discount", help="Discount percentage.")
@pass_context
def update_estimate(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update an estimate by ID."""
    client = ctx.get_client()
    estimate = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"estimates/{id}", json={"estimate": estimate})
    echo_output(data, fmt=ctx.output_format)


@estimates.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this estimate?")
@pass_context
def delete_estimate(ctx: Context, id: str) -> None:
    """Delete an estimate by ID."""
    client = ctx.get_client()
    client.delete(f"estimates/{id}")
    if not ctx.quiet:
        click.echo(f"Estimate {id} deleted.")


@estimates.command("send")
@click.argument("id")
@click.option("--delivery-method", type=click.Choice(["Email", "Simplerinvoicing", "Post", "Manual"]), default="Email", help="Delivery method.")
@click.option("--email-address", help="Override recipient email.")
@click.option("--email-message", help="Custom email message.")
@pass_context
def send_estimate(ctx: Context, id: str, delivery_method: str, email_address: str | None, email_message: str | None) -> None:
    """Send an estimate."""
    client = ctx.get_client()
    body: dict = {"delivery_method": delivery_method}
    if email_address:
        body["email_address"] = email_address
    if email_message:
        body["email_message"] = email_message
    data = client.patch(f"estimates/{id}/sends_an_estimate", json={"estimate_sending": body})
    echo_output(data, fmt=ctx.output_format)
