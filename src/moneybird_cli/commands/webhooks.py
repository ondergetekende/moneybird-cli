"""Webhooks commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "url", "events", "last_http_status", "last_http_body"]


@click.group()
def webhooks() -> None:
    """Manage webhooks."""


@webhooks.command("list")
@pass_context
def list_webhooks(ctx: Context) -> None:
    """List all webhooks."""
    client = ctx.get_client()
    data = client.get("webhooks")
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@webhooks.command("create")
@click.option("--url", required=True, help="Webhook URL.")
@click.option("--events", required=True, multiple=True, help="Event types to subscribe to (can be repeated).")
@pass_context
def create_webhook(ctx: Context, url: str, events: tuple[str, ...]) -> None:
    """Create a new webhook."""
    client = ctx.get_client()
    data = client.post("webhooks", json={"webhook": {"url": url, "events": list(events)}})
    echo_output(data, fmt=ctx.output_format)


@webhooks.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this webhook?")
@pass_context
def delete_webhook(ctx: Context, id: str) -> None:
    """Delete a webhook by ID."""
    client = ctx.get_client()
    client.delete(f"webhooks/{id}")
    if not ctx.quiet:
        click.echo(f"Webhook {id} deleted.")


@webhooks.command("activate")
@click.argument("id")
@pass_context
def activate_webhook(ctx: Context, id: str) -> None:
    """Activate a webhook by ID."""
    client = ctx.get_client()
    client.patch(f"webhooks/{id}/activate")
    if not ctx.quiet:
        click.echo(f"Webhook {id} activated.")


@webhooks.command("deactivate")
@click.argument("id")
@pass_context
def deactivate_webhook(ctx: Context, id: str) -> None:
    """Deactivate a webhook by ID."""
    client = ctx.get_client()
    client.patch(f"webhooks/{id}/deactivate")
    if not ctx.quiet:
        click.echo(f"Webhook {id} deactivated.")
