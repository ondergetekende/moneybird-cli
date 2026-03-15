"""Projects commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "name", "state", "budget"]


@click.group()
def projects() -> None:
    """Manage projects."""


@projects.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--state", type=click.Choice(["active", "archived", "all"]), default=None, help="Filter by state.")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_projects(ctx: Context, fetch_all: bool, state: str | None, page: int | None, per_page: int | None) -> None:
    """List projects. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    if state:
        params["filter"] = f"state:{state}"
    if fetch_all:
        data = client.get_all("projects", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("projects", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@projects.command("get")
@click.argument("id")
@pass_context
def get_project(ctx: Context, id: str) -> None:
    """Get a single project by ID."""
    client = ctx.get_client()
    data = client.get(f"projects/{id}")
    echo_output(data, fmt=ctx.output_format)


@projects.command("create")
@click.option("--name", required=True, help="Project name.")
@click.option("--budget", help="Project budget.")
@pass_context
def create_project(ctx: Context, name: str, budget: str | None) -> None:
    """Create a new project."""
    client = ctx.get_client()
    project: dict = {"name": name}
    if budget is not None:
        project["budget"] = budget
    data = client.post("projects", json={"project": project})
    echo_output(data, fmt=ctx.output_format)


@projects.command("update")
@click.argument("id")
@click.option("--name", help="Project name.")
@click.option("--budget", help="Project budget.")
@pass_context
def update_project(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a project by ID."""
    client = ctx.get_client()
    project = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"projects/{id}", json={"project": project})
    echo_output(data, fmt=ctx.output_format)


@projects.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this project?")
@pass_context
def delete_project(ctx: Context, id: str) -> None:
    """Delete a project by ID."""
    client = ctx.get_client()
    client.delete(f"projects/{id}")
    if not ctx.quiet:
        click.echo(f"Project {id} deleted.")
