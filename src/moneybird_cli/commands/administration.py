"""Administration-level resources: identities, downloads, users, workflows and other lookups."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output
from moneybird_cli.commands._common import clean, save_download


@click.command("custom-fields")
@pass_context
def custom_fields(ctx: Context) -> None:
    """List custom fields."""
    echo_output(ctx.get_client().get("custom_fields"), fmt=ctx.output_format, columns=["id", "name", "source"])


@click.command("document-styles")
@pass_context
def document_styles(ctx: Context) -> None:
    """List document styles."""
    echo_output(ctx.get_client().get("document_styles"), fmt=ctx.output_format, columns=["id", "name", "default"])


@click.command("verifications")
@pass_context
def verifications(ctx: Context) -> None:
    """List verified email addresses, bank accounts and other verifications."""
    echo_output(ctx.get_client().get("verifications"), fmt=ctx.output_format)


@click.command("users")
@click.option("--include-inactive", is_flag=True, default=None, help="Include inactive users.")
@click.option("--include-accountants", is_flag=True, default=None, help="Include accountants.")
@click.option("--include-api-users", is_flag=True, default=None, help="Include API users.")
@pass_context
def users(ctx: Context, **kwargs: bool | None) -> None:
    """List users of the administration."""
    data = ctx.get_client().get("users", params=clean(kwargs))
    echo_output(data, fmt=ctx.output_format, columns=["id", "name", "email", "user_type"])


# --- Workflows ---

@click.group()
def workflows() -> None:
    """View workflows."""


@workflows.command("list")
@pass_context
def list_workflows(ctx: Context) -> None:
    """List workflows."""
    echo_output(ctx.get_client().get("workflows"), fmt=ctx.output_format, columns=["id", "type", "name", "default", "active"])


@workflows.command("get")
@click.argument("id")
@pass_context
def get_workflow(ctx: Context, id: str) -> None:
    """Get a workflow by ID."""
    echo_output(ctx.get_client().get(f"workflows/{id}"), fmt=ctx.output_format)


# --- Downloads ---

@click.group()
def downloads() -> None:
    """List and fetch generated exports."""


@downloads.command("list")
@click.option("--type", "download_type", help="Filter by type (e.g., auditfile, brugstaat).")
@click.option("--downloaded/--not-downloaded", default=None, help="Filter by downloaded state.")
@click.option("--failed/--not-failed", default=None, help="Filter by failed state.")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@pass_context
def list_downloads(ctx: Context, **kwargs: str | bool | int | None) -> None:
    """List downloads."""
    data = ctx.get_client().get("downloads", params=clean(kwargs))
    echo_output(data, fmt=ctx.output_format, columns=["id", "filename", "download_type", "downloaded", "failed", "created_at"])


@downloads.command("get")
@click.argument("id")
@click.option("--output", "output_path", type=click.Path(), required=True, help="Output file path.")
@pass_context
def get_download(ctx: Context, id: str, output_path: str) -> None:
    """Download a generated file."""
    save_download(ctx, ctx.get_client(), f"downloads/{id}/download", output_path, method="POST")


# --- Identities ---

IDENTITY_FIELDS = ["company_name", "address1", "address2", "zipcode", "city", "country", "email", "phone",
                   "bank_account_name", "bank_account_number", "bank_account_bic"]


def _identity_options(required: bool):
    def decorate(f):
        for field in reversed(IDENTITY_FIELDS):
            needed = required and field in ("company_name", "address1", "zipcode", "city", "country", "email")
            f = click.option(f"--{field.replace('_', '-')}", field, required=needed)(f)
        return f
    return decorate


@click.group()
def identities() -> None:
    """Manage identities (the company details shown on invoices)."""


@identities.command("list")
@pass_context
def list_identities(ctx: Context) -> None:
    """List identities."""
    echo_output(ctx.get_client().get("identities"), fmt=ctx.output_format, columns=["id", "company_name", "city", "email"])


@identities.command("get")
@click.argument("id", default="default")
@pass_context
def get_identity(ctx: Context, id: str) -> None:
    """Get an identity by ID (default: the default identity)."""
    echo_output(ctx.get_client().get(f"identities/{id}"), fmt=ctx.output_format)


@identities.command("create")
@_identity_options(required=True)
@pass_context
def create_identity(ctx: Context, **kwargs: str | None) -> None:
    """Create an identity."""
    echo_output(ctx.get_client().post("identities", json={"identity": clean(kwargs)}), fmt=ctx.output_format)


@identities.command("update")
@click.argument("id", default="default")
@_identity_options(required=False)
@click.option("--chamber-of-commerce", help="Chamber of commerce number (default identity only).")
@click.option("--tax-number", help="VAT number (default identity only).")
@pass_context
def update_identity(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update an identity (default: the default identity)."""
    data = ctx.get_client().patch(f"identities/{id}", json={"identity": clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@identities.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this identity?")
@pass_context
def delete_identity(ctx: Context, id: str) -> None:
    """Delete an identity."""
    ctx.get_client().delete(f"identities/{id}")
    if not ctx.quiet:
        click.echo(f"Identity {id} deleted.")
