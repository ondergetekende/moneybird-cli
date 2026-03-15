"""Contacts commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

LIST_COLUMNS = ["id", "company_name", "firstname", "lastname", "email"]


@click.group()
def contacts() -> None:
    """Manage contacts."""


@contacts.command("list")
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
@click.option("--include-archived", is_flag=True, help="Include archived contacts.")
@pass_context
def list_contacts(ctx: Context, fetch_all: bool, page: int | None, per_page: int | None, include_archived: bool) -> None:
    """List contacts. Returns the first page by default; use --all to fetch everything."""
    client = ctx.get_client()
    params: dict = {}
    if include_archived:
        params["include_archived"] = "true"
    if fetch_all:
        data = client.get_all("contacts", params=params, per_page=per_page or 100)
    else:
        params["page"] = page or 1
        if per_page:
            params["per_page"] = per_page
        data = client.get("contacts", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@contacts.command("get")
@click.argument("id")
@pass_context
def get_contact(ctx: Context, id: str) -> None:
    """Get a single contact by ID."""
    client = ctx.get_client()
    data = client.get(f"contacts/{id}")
    echo_output(data, fmt=ctx.output_format)


@contacts.command("search")
@click.argument("query")
@pass_context
def search_contacts(ctx: Context, query: str) -> None:
    """Search contacts by name or email."""
    client = ctx.get_client()
    data = client.get_all("contacts", params={"query": query})
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@contacts.command("filter")
@click.option("--created-after", help="Filter by creation date (ISO 8601).")
@click.option("--updated-after", help="Filter by update date (ISO 8601).")
@click.option("--first-name", help="Filter by first name.")
@click.option("--last-name", help="Filter by last name.")
@pass_context
def filter_contacts(
    ctx: Context,
    created_after: str | None,
    updated_after: str | None,
    first_name: str | None,
    last_name: str | None,
) -> None:
    """Filter contacts by criteria."""
    client = ctx.get_client()
    params: dict = {}
    if created_after:
        params["filter"] = f"created_after:{created_after}"
    if updated_after:
        params["filter"] = f"updated_after:{updated_after}"
    if first_name:
        params["filter"] = f"first_name:{first_name}"
    if last_name:
        params["filter"] = f"last_name:{last_name}"
    data = client.get_all("contacts/filter", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@contacts.command("create")
@click.option("--company-name", help="Company name.")
@click.option("--firstname", help="First name.")
@click.option("--lastname", help="Last name.")
@click.option("--email", help="Email address.")
@click.option("--phone", help="Phone number.")
@click.option("--address1", help="Address line 1.")
@click.option("--address2", help="Address line 2.")
@click.option("--zipcode", help="Zip code.")
@click.option("--city", help="City.")
@click.option("--country", help="Country code (e.g., NL).")
@click.option("--delivery-method", type=click.Choice(["Email", "Simplerinvoicing", "Post", "Manual"]), help="Invoice delivery method.")
@pass_context
def create_contact(ctx: Context, **kwargs: str | None) -> None:
    """Create a new contact."""
    client = ctx.get_client()
    contact = {k.replace("_", ""): v for k, v in kwargs.items() if v is not None}
    # Map back to API field names
    field_map = {
        "companyname": "company_name",
        "address1": "address1",
        "address2": "address2",
        "deliverymethod": "delivery_method",
    }
    api_contact = {}
    for k, v in contact.items():
        api_contact[field_map.get(k, k)] = v
    data = client.post("contacts", json={"contact": api_contact})
    echo_output(data, fmt=ctx.output_format)


@contacts.command("update")
@click.argument("id")
@click.option("--company-name", help="Company name.")
@click.option("--firstname", help="First name.")
@click.option("--lastname", help="Last name.")
@click.option("--email", help="Email address.")
@click.option("--phone", help="Phone number.")
@pass_context
def update_contact(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a contact by ID."""
    client = ctx.get_client()
    contact = {k: v for k, v in kwargs.items() if v is not None}
    field_map = {"company_name": "company_name"}
    api_contact = {}
    for k, v in contact.items():
        api_contact[field_map.get(k, k)] = v
    data = client.patch(f"contacts/{id}", json={"contact": api_contact})
    echo_output(data, fmt=ctx.output_format)


@contacts.command("delete")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this contact?")
@pass_context
def delete_contact(ctx: Context, id: str) -> None:
    """Delete a contact by ID."""
    client = ctx.get_client()
    client.delete(f"contacts/{id}")
    if not ctx.quiet:
        click.echo(f"Contact {id} deleted.")


@contacts.command("archive")
@click.argument("id")
@pass_context
def archive_contact(ctx: Context, id: str) -> None:
    """Archive a contact by ID."""
    client = ctx.get_client()
    client.patch(f"contacts/{id}/archive")
    if not ctx.quiet:
        click.echo(f"Contact {id} archived.")
