"""Subscriptions commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output
from moneybird_cli.commands._common import add_additional_charges, clean

LIST_COLUMNS = ["id", "contact_id", "start_date", "end_date", "cancelled_at", "frequency_type", "frequency"]


@click.group()
def subscriptions() -> None:
    """Manage subscriptions."""


@subscriptions.command("list")
@click.option("--contact-id", required=True, help="Contact ID (upstream only lists per contact).")
@pass_context
def list_subscriptions(ctx: Context, contact_id: str) -> None:
    """List subscriptions of a contact."""
    client = ctx.get_client()
    data = client.get("subscriptions", params={"contact_id": contact_id})
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@subscriptions.command("get")
@click.argument("id")
@pass_context
def get_subscription(ctx: Context, id: str) -> None:
    """Get a single subscription by ID."""
    client = ctx.get_client()
    data = client.get(f"subscriptions/{id}")
    echo_output(data, fmt=ctx.output_format)


@subscriptions.command("create")
@click.option("--contact-id", required=True, help="Contact ID.")
@click.option("--start-date", help="Start date (YYYY-MM-DD).")
@click.option("--end-date", help="End date (YYYY-MM-DD).")
@click.option("--frequency-type", type=click.Choice(["day", "week", "month", "quarter", "year"]), help="Frequency type.")
@click.option("--frequency", type=int, help="Frequency interval.")
@click.option("--product-id", help="Product ID.")
@pass_context
def create_subscription(ctx: Context, **kwargs: str | int | None) -> None:
    """Create a new subscription."""
    client = ctx.get_client()
    sub = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("subscriptions", json={"subscription": sub})
    echo_output(data, fmt=ctx.output_format)


@subscriptions.command("update")
@click.argument("id")
@click.option("--start-date", help="Start date (YYYY-MM-DD).")
@click.option("--product-id", help="Product ID.")
@click.option("--reference", help="Reference.")
@pass_context
def update_subscription(ctx: Context, id: str, **kwargs: str | int | None) -> None:
    """Update a subscription by ID."""
    client = ctx.get_client()
    sub = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"subscriptions/{id}", json={"subscription": sub})
    echo_output(data, fmt=ctx.output_format)


@subscriptions.command("cancel")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to cancel this subscription?")
@pass_context
def cancel_subscription(ctx: Context, id: str) -> None:
    """Cancel a subscription by ID."""
    client = ctx.get_client()
    client.delete(f"subscriptions/{id}")
    if not ctx.quiet:
        click.echo(f"Subscription {id} cancelled.")


@subscriptions.command("schedule-invoice")
@click.argument("id")
@click.option("--description", required=True, help="Invoice line description.")
@click.option("--price", required=True, help="Price.")
@click.option("--amount", help="Amount, e.g. '1' or '3 x'.")
@click.option("--product-id", help="Product ID.")
@click.option("--invoice-date", help="Invoice date (YYYY-MM-DD).")
@pass_context
def schedule_invoice(ctx: Context, id: str, invoice_date: str | None, **line: str | None) -> None:
    """Create a one-off invoice that is sent together with the subscription's next invoice."""
    invoice = clean({"invoice_date": invoice_date, "details_attributes": [clean(line)]})
    data = ctx.get_client().post(f"subscriptions/{id}/create_and_schedule_one_off_sales_invoice", json={"sales_invoice": invoice})
    echo_output(data, fmt=ctx.output_format)


@subscriptions.command("templates")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@pass_context
def list_templates(ctx: Context, fetch_all: bool) -> None:
    """List subscription templates."""
    client = ctx.get_client()
    data = client.get_all("subscription_templates") if fetch_all else client.get("subscription_templates")
    echo_output(data, fmt=ctx.output_format)


@subscriptions.command("template-link")
@click.argument("template_id")
@click.option("--contact-id", help="Pre-fill for this contact.")
@click.option("--product-id", help="Product ID.")
@click.option("--start-date", help="Start date (YYYY-MM-DD).")
@pass_context
def template_link(ctx: Context, template_id: str, **kwargs: str | None) -> None:
    """Create an online sales link for a subscription template."""
    data = ctx.get_client().post(f"subscription_templates/{template_id}/sales_link", params=clean(kwargs))
    echo_output(data, fmt=ctx.output_format)


add_additional_charges(subscriptions, "subscriptions")
