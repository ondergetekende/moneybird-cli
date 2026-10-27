"""Task list commands (task lists, templates, groups, tasks)."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

REPORT_TYPES = click.Choice(["balance_sheet", "profit_loss", "debtor", "creditor", "assets"])


def _clean(kwargs: dict) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


def _deleted(ctx: Context, what: str, id: str) -> None:
    if not ctx.quiet:
        click.echo(f"{what} {id} deleted.")


@click.group(name="task-lists")
def task_lists() -> None:
    """Manage task lists (closing checklists), their groups, tasks and templates."""


@task_lists.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_task_lists(ctx: Context, fetch_all: bool, page: int | None, per_page: int | None) -> None:
    """List task lists."""
    client = ctx.get_client()
    if fetch_all:
        data = client.get_all("task_lists", per_page=per_page or 100)
    else:
        data = client.get("task_lists", params=_clean({"page": page or 1, "per_page": per_page}))
    echo_output(data, fmt=ctx.output_format, columns=["id", "name", "deadline_on", "period_begin", "period_end"])


@task_lists.command("get")
@click.argument("id")
@pass_context
def get_task_list(ctx: Context, id: str) -> None:
    """Get a task list by ID."""
    echo_output(ctx.get_client().get(f"task_lists/{id}"), fmt=ctx.output_format)


@task_lists.command("create")
@click.option("--name", required=True, help="Name.")
@click.option("--description", help="Description.")
@click.option("--deadline-on", help="Deadline (YYYY-MM-DD).")
@click.option("--period-begin", help="Period start (YYYY-MM-DD).")
@click.option("--period-end", help="Period end (YYYY-MM-DD).")
@click.option("--template-id", help="Create from this template.")
@pass_context
def create_task_list(ctx: Context, **kwargs: str | None) -> None:
    """Create a task list."""
    data = ctx.get_client().post("task_lists", json={"task_list": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@task_lists.command("update")
@click.argument("id")
@click.option("--name", help="Name.")
@click.option("--description", help="Description.")
@click.option("--deadline-on", help="Deadline (YYYY-MM-DD).")
@pass_context
def update_task_list(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a task list."""
    data = ctx.get_client().patch(f"task_lists/{id}", json={"task_list": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@task_lists.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this task list?")
@pass_context
def delete_task_list(ctx: Context, id: str) -> None:
    """Delete a task list."""
    ctx.get_client().delete(f"task_lists/{id}")
    _deleted(ctx, "Task list", id)


@task_lists.command("add-group")
@click.argument("task_list_id")
@click.option("--name", required=True, help="Group name.")
@click.option("--report-type", type=REPORT_TYPES, help="Linked report type.")
@pass_context
def add_group(ctx: Context, task_list_id: str, **kwargs: str | None) -> None:
    """Add a group to a task list."""
    data = ctx.get_client().post(f"task_lists/{task_list_id}/groups", json={"group": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


# --- Templates ---

@task_lists.group("templates")
def templates() -> None:
    """Manage task list templates."""


@templates.command("list")
@pass_context
def list_templates(ctx: Context) -> None:
    """List task list templates."""
    data = ctx.get_client().get("task_list_templates")
    echo_output(data, fmt=ctx.output_format, columns=["id", "name", "period", "deadline_after"])


@templates.command("get")
@click.argument("id")
@pass_context
def get_template(ctx: Context, id: str) -> None:
    """Get a task list template by ID."""
    echo_output(ctx.get_client().get(f"task_list_templates/{id}"), fmt=ctx.output_format)


@templates.command("create")
@click.option("--name", required=True, help="Name.")
@click.option("--description", help="Description.")
@click.option("--period", help="Recurrence period.")
@click.option("--deadline-after", help="Deadline offset after the period.")
@pass_context
def create_template(ctx: Context, **kwargs: str | None) -> None:
    """Create a task list template."""
    data = ctx.get_client().post("task_list_templates", json={"task_list_template": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@templates.command("update")
@click.argument("id")
@click.option("--name", help="Name.")
@click.option("--description", help="Description.")
@click.option("--period", help="Recurrence period.")
@click.option("--deadline-after", help="Deadline offset after the period.")
@pass_context
def update_template(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a task list template."""
    data = ctx.get_client().patch(f"task_list_templates/{id}", json={"task_list_template": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@templates.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this template?")
@pass_context
def delete_template(ctx: Context, id: str) -> None:
    """Delete a task list template."""
    ctx.get_client().delete(f"task_list_templates/{id}")
    _deleted(ctx, "Template", id)


@templates.command("add-group")
@click.argument("template_id")
@click.option("--name", required=True, help="Group name.")
@click.option("--report-type", type=REPORT_TYPES, help="Linked report type.")
@pass_context
def add_template_group(ctx: Context, template_id: str, **kwargs: str | None) -> None:
    """Add a group to a task list template."""
    data = ctx.get_client().post(f"task_list_templates/{template_id}/groups", json={"group": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@templates.command("instantiate")
@click.argument("template_id")
@click.option("--name", help="Name.")
@click.option("--description", help="Description.")
@click.option("--deadline-on", help="Deadline (YYYY-MM-DD).")
@click.option("--period-begin", help="Period start (YYYY-MM-DD).")
@click.option("--period-end", help="Period end (YYYY-MM-DD).")
@pass_context
def instantiate_template(ctx: Context, template_id: str, **kwargs: str | None) -> None:
    """Create a task list from a template."""
    data = ctx.get_client().post(f"task_list_templates/{template_id}/task_lists", json={"task_list": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


# --- Groups ---

@task_lists.group("groups")
def groups() -> None:
    """Manage groups within task lists and templates."""


@groups.command("get")
@click.argument("id")
@pass_context
def get_group(ctx: Context, id: str) -> None:
    """Get a group by ID."""
    echo_output(ctx.get_client().get(f"task_list_groups/{id}"), fmt=ctx.output_format)


@groups.command("update")
@click.argument("id")
@click.option("--name", help="Group name.")
@click.option("--report-type", type=REPORT_TYPES, help="Linked report type.")
@pass_context
def update_group(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a group."""
    data = ctx.get_client().patch(f"task_list_groups/{id}", json={"group": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@groups.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this group?")
@pass_context
def delete_group(ctx: Context, id: str) -> None:
    """Delete a group."""
    ctx.get_client().delete(f"task_list_groups/{id}")
    _deleted(ctx, "Group", id)


@groups.command("add-task")
@click.argument("group_id")
@click.option("--name", required=True, help="Task name.")
@click.option("--description", help="Description.")
@click.option("--report-type", type=REPORT_TYPES, help="Linked report type.")
@click.option("--assignee-id", help="User ID to assign.")
@click.option("--related-entity-id", help="Related entity ID.")
@click.option("--generate-subtasks", is_flag=True, default=None, help="Generate subtasks.")
@pass_context
def add_task(ctx: Context, group_id: str, **kwargs: str | bool | None) -> None:
    """Add a task to a group."""
    data = ctx.get_client().post(f"task_list_groups/{group_id}/tasks", json={"task": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


# --- Tasks ---

@task_lists.group("tasks")
def tasks() -> None:
    """Manage individual tasks."""


@tasks.command("get")
@click.argument("id")
@pass_context
def get_task(ctx: Context, id: str) -> None:
    """Get a task by ID."""
    echo_output(ctx.get_client().get(f"task_list_tasks/{id}"), fmt=ctx.output_format)


@tasks.command("update")
@click.argument("id")
@click.option("--name", help="Task name.")
@click.option("--description", help="Description.")
@click.option("--report-type", type=REPORT_TYPES, help="Linked report type.")
@click.option("--assignee-id", help="User ID to assign.")
@click.option("--related-entity-id", help="Related entity ID.")
@pass_context
def update_task(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a task."""
    data = ctx.get_client().patch(f"task_list_tasks/{id}", json={"task": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@tasks.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this task?")
@pass_context
def delete_task(ctx: Context, id: str) -> None:
    """Delete a task."""
    ctx.get_client().delete(f"task_list_tasks/{id}")
    _deleted(ctx, "Task", id)


@tasks.command("assign")
@click.argument("id")
@click.argument("assignee_id")
@pass_context
def assign_task(ctx: Context, id: str, assignee_id: str) -> None:
    """Assign a user to a task."""
    data = ctx.get_client().post(f"task_list_tasks/{id}/assignment", json={"assignee_id": assignee_id})
    echo_output(data, fmt=ctx.output_format)


@tasks.command("unassign")
@click.argument("id")
@pass_context
def unassign_task(ctx: Context, id: str) -> None:
    """Remove the assignee from a task."""
    data = ctx.get_client().delete(f"task_list_tasks/{id}/assignment")
    echo_output(data, fmt=ctx.output_format)


@tasks.command("complete")
@click.argument("id")
@pass_context
def complete_task(ctx: Context, id: str) -> None:
    """Mark a task as completed."""
    data = ctx.get_client().post(f"task_list_tasks/{id}/completion")
    echo_output(data, fmt=ctx.output_format)


@tasks.command("reopen")
@click.argument("id")
@pass_context
def reopen_task(ctx: Context, id: str) -> None:
    """Mark a completed task as not completed."""
    data = ctx.get_client().delete(f"task_list_tasks/{id}/completion")
    echo_output(data, fmt=ctx.output_format)


@tasks.command("note")
@click.argument("id")
@click.argument("note")
@click.option("--todo", is_flag=True, default=None, help="Mark the note as a to-do.")
@pass_context
def add_task_note(ctx: Context, id: str, **kwargs: str | bool | None) -> None:
    """Add a note to a task."""
    data = ctx.get_client().post(f"task_list_tasks/{id}/notes", json={"note": _clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)
