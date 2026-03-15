"""Time entries commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "contact_id", "project_id", "started_at", "ended_at", "description", "billable"]


@click.group(name="time-entries")
def time_entries() -> None:
    """Manage time entries."""


@time_entries.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_time_entries(ctx: Context, fetch_all: bool, page: int | None, per_page: int | None) -> None:
    """List time entries. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    if fetch_all:
        data = client.get_all("time_entries", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("time_entries", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@time_entries.command("get")
@click.argument("id")
@pass_context
def get_time_entry(ctx: Context, id: str) -> None:
    """Get a single time entry by ID."""
    client = ctx.get_client()
    data = client.get(f"time_entries/{id}")
    echo_output(data, fmt=ctx.output_format)


@time_entries.command("create")
@click.option("--started-at", required=True, help="Start time (ISO 8601).")
@click.option("--ended-at", required=True, help="End time (ISO 8601).")
@click.option("--description", help="Description of work.")
@click.option("--contact-id", help="Contact ID.")
@click.option("--project-id", help="Project ID.")
@click.option("--billable", is_flag=True, default=None, help="Mark as billable.")
@pass_context
def create_time_entry(ctx: Context, **kwargs: str | bool | None) -> None:
    """Create a new time entry."""
    client = ctx.get_client()
    entry = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("time_entries", json={"time_entry": entry})
    echo_output(data, fmt=ctx.output_format)


@time_entries.command("update")
@click.argument("id")
@click.option("--started-at", help="Start time (ISO 8601).")
@click.option("--ended-at", help="End time (ISO 8601).")
@click.option("--description", help="Description of work.")
@click.option("--contact-id", help="Contact ID.")
@click.option("--project-id", help="Project ID.")
@pass_context
def update_time_entry(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a time entry by ID."""
    client = ctx.get_client()
    entry = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"time_entries/{id}", json={"time_entry": entry})
    echo_output(data, fmt=ctx.output_format)


@time_entries.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this time entry?")
@pass_context
def delete_time_entry(ctx: Context, id: str) -> None:
    """Delete a time entry by ID."""
    client = ctx.get_client()
    client.delete(f"time_entries/{id}")
    if not ctx.quiet:
        click.echo(f"Time entry {id} deleted.")
