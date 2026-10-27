"""Contacts commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output
from moneybird_cli.commands._common import add_additional_charges, add_notes, add_sync, clean

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
    filters = []
    if created_after:
        filters.append(f"created_after:{created_after}")
    if updated_after:
        filters.append(f"updated_after:{updated_after}")
    if first_name:
        filters.append(f"first_name:{first_name}")
    if last_name:
        filters.append(f"last_name:{last_name}")
    params = {"filter": ",".join(filters)} if filters else {}
    data = client.get_all("contacts/filter", params=params)
    echo_output(data, fmt=ctx.output_format, columns=LIST_COLUMNS)


@contacts.command("doubles")
@click.option("--page", type=int, default=None, help="Page number (default: 1).")
@pass_context
def contact_doubles(ctx: Context, page: int | None) -> None:
    """List groups of possible duplicate contacts."""
    client = ctx.get_client()
    data = client.get("contacts/doubles", params={"page": page or 1})
    echo_output(data, fmt=ctx.output_format)


@contacts.command("create")
@click.option("--company-name", help="Company name.")
@click.option("--firstname", help="First name.")
@click.option("--lastname", help="Last name.")
@click.option("--email", help="Email address invoices are sent to.")
@click.option("--phone", help="Phone number.")
@click.option("--address1", help="Address line 1.")
@click.option("--address2", help="Address line 2.")
@click.option("--zipcode", help="Zip code.")
@click.option("--city", help="City.")
@click.option("--country", help="Country code (e.g., NL).")
@click.option("--delivery-method", type=click.Choice(["Email", "Peppol", "Post", "Manual"]), help="Invoice delivery method.")
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
        "email": "send_invoices_to_email",
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
@click.option("--email", help="Email address invoices are sent to.")
@click.option("--phone", help="Phone number.")
@pass_context
def update_contact(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a contact by ID."""
    client = ctx.get_client()
    contact = {k: v for k, v in kwargs.items() if v is not None}
    field_map = {"email": "send_invoices_to_email"}
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


@contacts.command("find")
@click.argument("customer_id")
@pass_context
def find_contact(ctx: Context, customer_id: str) -> None:
    """Find a contact by its customer ID."""
    echo_output(ctx.get_client().get(f"contacts/customer_id/{customer_id}"), fmt=ctx.output_format)


@contacts.command("portal-link")
@click.argument("id")
@click.option("--invoices", is_flag=True, help="Link to the invoices page.")
@click.option("--subscription-id", help="Link to this subscription.")
@pass_context
def portal_link(ctx: Context, id: str, invoices: bool, subscription_id: str | None) -> None:
    """Get a temporary link to the customer portal of a contact."""
    path = f"customer_contact_portal/{id}"
    if subscription_id:
        path += f"/subscriptions/{subscription_id}"
    elif invoices:
        path += "/invoices"
    echo_output(ctx.get_client().get(path), fmt=ctx.output_format)


# --- Contact people ---

PERSON_OPTIONS = [
    click.option("--firstname", help="First name."),
    click.option("--lastname", help="Last name."),
    click.option("--phone", help="Phone number."),
    click.option("--email", help="Email address."),
    click.option("--department", help="Department."),
]


def _person_options(f):
    for option in reversed(PERSON_OPTIONS):
        f = option(f)
    return f


@contacts.group("people")
def people() -> None:
    """Manage contact people of a contact."""


@people.command("get")
@click.argument("contact_id")
@click.argument("id")
@pass_context
def get_person(ctx: Context, contact_id: str, id: str) -> None:
    """Get a contact person."""
    echo_output(ctx.get_client().get(f"contacts/{contact_id}/contact_people/{id}"), fmt=ctx.output_format)


@people.command("create")
@click.argument("contact_id")
@_person_options
@pass_context
def create_person(ctx: Context, contact_id: str, **kwargs: str | None) -> None:
    """Add a contact person to a contact."""
    data = ctx.get_client().post(f"contacts/{contact_id}/contact_people", json={"contact_person": clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@people.command("update")
@click.argument("contact_id")
@click.argument("id")
@_person_options
@pass_context
def update_person(ctx: Context, contact_id: str, id: str, **kwargs: str | None) -> None:
    """Update a contact person."""
    data = ctx.get_client().patch(f"contacts/{contact_id}/contact_people/{id}", json={"contact_person": clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@people.command("delete")
@click.argument("contact_id")
@click.argument("id")
@click.confirmation_option(prompt="Are you sure you want to delete this contact person?")
@pass_context
def delete_person(ctx: Context, contact_id: str, id: str) -> None:
    """Delete a contact person."""
    ctx.get_client().delete(f"contacts/{contact_id}/contact_people/{id}")
    if not ctx.quiet:
        click.echo(f"Contact person {id} deleted.")


# --- Moneybird Payments mandate ---

@contacts.group("mandate")
def mandate() -> None:
    """Manage the Moneybird Payments direct-debit mandate of a contact."""


@mandate.command("get")
@click.argument("contact_id")
@pass_context
def get_mandate(ctx: Context, contact_id: str) -> None:
    """Show the mandate of a contact."""
    echo_output(ctx.get_client().get(f"contacts/{contact_id}/moneybird_payments_mandate"), fmt=ctx.output_format)


@mandate.command("request")
@click.argument("contact_id")
@click.option("--email-message", help="Custom email message.")
@click.option("--identity-id", help="Identity ID.")
@click.option("--workflow-id", help="Workflow ID.")
@pass_context
def request_mandate(ctx: Context, contact_id: str, **kwargs: str | None) -> None:
    """Email the contact a request to set up a mandate."""
    ctx.get_client().post(f"contacts/{contact_id}/moneybird_payments_mandate", json={"mandate_request": clean(kwargs)})
    if not ctx.quiet:
        click.echo("Mandate requested.")


@mandate.command("url")
@click.argument("contact_id")
@click.option("--identity-id", help="Identity ID.")
@click.option("--workflow-id", help="Workflow ID.")
@pass_context
def mandate_url(ctx: Context, contact_id: str, **kwargs: str | None) -> None:
    """Get a URL where the contact can set up a mandate."""
    data = ctx.get_client().post(f"contacts/{contact_id}/moneybird_payments_mandate/url", json={"mandate_request": clean(kwargs)})
    echo_output(data, fmt=ctx.output_format)


@mandate.command("delete")
@click.argument("contact_id")
@click.confirmation_option(prompt="Are you sure you want to delete this mandate?")
@pass_context
def delete_mandate(ctx: Context, contact_id: str) -> None:
    """Delete the mandate of a contact."""
    ctx.get_client().delete(f"contacts/{contact_id}/moneybird_payments_mandate")
    if not ctx.quiet:
        click.echo("Mandate deleted.")


add_sync(contacts, "contacts", LIST_COLUMNS)
add_notes(contacts, "contacts")
add_additional_charges(contacts, "contacts")
