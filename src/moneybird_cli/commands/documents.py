"""Document commands (general, journal, purchase invoices, receipts, typeless)."""

from __future__ import annotations

from typing import Any, Callable

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output


def _list_cmd(api_path: str, list_columns: list[str]) -> Callable:
    @click.command("list")
    @click.option("--all", "fetch_all", is_flag=True, help="Fetch all pages (respects rate limits).")
    @click.option("--page", type=int, default=None, help="Page number (default: 1).")
    @click.option("--per-page", type=int, default=None, help="Results per page (max 100).")
    @pass_context
    def cmd(ctx: Context, fetch_all: bool, page: int | None, per_page: int | None) -> None:
        """List documents. Returns the first page by default; use --all to fetch everything."""
        client = ctx.get_client()
        params: dict = {}
        if fetch_all:
            data = client.get_all(api_path, params=params, per_page=per_page or 100)
        else:
            params["page"] = page or 1
            if per_page:
                params["per_page"] = per_page
            data = client.get(api_path, params=params)
        echo_output(data, fmt=ctx.output_format, columns=list_columns)
    return cmd


def _get_cmd(api_path: str) -> Callable:
    @click.command("get")
    @click.argument("id")
    @pass_context
    def cmd(ctx: Context, id: str) -> None:
        """Get a single document by ID."""
        client = ctx.get_client()
        data = client.get(f"{api_path}/{id}")
        echo_output(data, fmt=ctx.output_format)
    return cmd


def _delete_cmd(api_path: str) -> Callable:
    @click.command("delete")
    @click.argument("id")
    @click.confirmation_option(prompt="Are you sure you want to delete this document?")
    @pass_context
    def cmd(ctx: Context, id: str) -> None:
        """Delete a document by ID."""
        client = ctx.get_client()
        client.delete(f"{api_path}/{id}")
        if not ctx.quiet:
            click.echo(f"Document {id} deleted.")
    return cmd


# --- General Documents ---

@click.group(name="general-documents")
def general_documents() -> None:
    """Manage general documents."""

general_documents.add_command(_list_cmd("documents/general_documents", ["id", "contact_id", "reference", "date", "state"]))
general_documents.add_command(_get_cmd("documents/general_documents"))
general_documents.add_command(_delete_cmd("documents/general_documents"))

@general_documents.command("create")
@click.option("--contact-id", required=True, help="Contact ID.")
@click.option("--reference", help="Document reference.")
@click.option("--date", help="Document date (YYYY-MM-DD).")
@click.option("--due-date", help="Due date (YYYY-MM-DD).")
@pass_context
def create_general_document(ctx: Context, **kwargs: str | None) -> None:
    """Create a new general document."""
    client = ctx.get_client()
    doc = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("documents/general_documents", json={"general_document": doc})
    echo_output(data, fmt=ctx.output_format)

@general_documents.command("update")
@click.argument("id")
@click.option("--reference", help="Document reference.")
@click.option("--date", help="Document date (YYYY-MM-DD).")
@click.option("--due-date", help="Due date (YYYY-MM-DD).")
@pass_context
def update_general_document(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a general document by ID."""
    client = ctx.get_client()
    doc = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"documents/general_documents/{id}", json={"general_document": doc})
    echo_output(data, fmt=ctx.output_format)


# --- General Journal Documents ---

@click.group(name="journal-documents")
def general_journal_documents() -> None:
    """Manage general journal documents."""

general_journal_documents.add_command(_list_cmd("documents/general_journal_documents", ["id", "reference", "date", "journal_type"]))
general_journal_documents.add_command(_get_cmd("documents/general_journal_documents"))
general_journal_documents.add_command(_delete_cmd("documents/general_journal_documents"))

@general_journal_documents.command("create")
@click.option("--reference", help="Document reference.")
@click.option("--date", help="Document date (YYYY-MM-DD).")
@pass_context
def create_journal_document(ctx: Context, **kwargs: str | None) -> None:
    """Create a new general journal document."""
    client = ctx.get_client()
    doc = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("documents/general_journal_documents", json={"general_journal_document": doc})
    echo_output(data, fmt=ctx.output_format)

@general_journal_documents.command("update")
@click.argument("id")
@click.option("--reference", help="Document reference.")
@click.option("--date", help="Document date (YYYY-MM-DD).")
@pass_context
def update_journal_document(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a general journal document by ID."""
    client = ctx.get_client()
    doc = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"documents/general_journal_documents/{id}", json={"general_journal_document": doc})
    echo_output(data, fmt=ctx.output_format)


# --- Purchase Invoices ---

@click.group(name="purchase-invoices")
def purchase_invoices() -> None:
    """Manage purchase invoices."""

purchase_invoices.add_command(_list_cmd("documents/purchase_invoices", ["id", "contact_id", "reference", "date", "state", "total_price_incl_tax"]))
purchase_invoices.add_command(_get_cmd("documents/purchase_invoices"))
purchase_invoices.add_command(_delete_cmd("documents/purchase_invoices"))

@purchase_invoices.command("create")
@click.option("--contact-id", required=True, help="Contact ID.")
@click.option("--reference", help="Invoice reference.")
@click.option("--date", help="Invoice date (YYYY-MM-DD).")
@click.option("--due-date", help="Due date (YYYY-MM-DD).")
@click.option("--currency", help="Currency code (default: EUR).")
@pass_context
def create_purchase_invoice(ctx: Context, **kwargs: str | None) -> None:
    """Create a new purchase invoice."""
    client = ctx.get_client()
    doc = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("documents/purchase_invoices", json={"purchase_invoice": doc})
    echo_output(data, fmt=ctx.output_format)

@purchase_invoices.command("update")
@click.argument("id")
@click.option("--reference", help="Invoice reference.")
@click.option("--date", help="Invoice date (YYYY-MM-DD).")
@click.option("--due-date", help="Due date (YYYY-MM-DD).")
@pass_context
def update_purchase_invoice(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a purchase invoice by ID."""
    client = ctx.get_client()
    doc = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"documents/purchase_invoices/{id}", json={"purchase_invoice": doc})
    echo_output(data, fmt=ctx.output_format)


# --- Receipts ---

@click.group(name="receipts")
def receipts() -> None:
    """Manage receipts."""

receipts.add_command(_list_cmd("documents/receipts", ["id", "contact_id", "reference", "date", "state", "total_price_incl_tax"]))
receipts.add_command(_get_cmd("documents/receipts"))
receipts.add_command(_delete_cmd("documents/receipts"))

@receipts.command("create")
@click.option("--contact-id", required=True, help="Contact ID.")
@click.option("--reference", help="Receipt reference.")
@click.option("--date", help="Receipt date (YYYY-MM-DD).")
@pass_context
def create_receipt(ctx: Context, **kwargs: str | None) -> None:
    """Create a new receipt."""
    client = ctx.get_client()
    doc = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("documents/receipts", json={"receipt": doc})
    echo_output(data, fmt=ctx.output_format)

@receipts.command("update")
@click.argument("id")
@click.option("--reference", help="Receipt reference.")
@click.option("--date", help="Receipt date (YYYY-MM-DD).")
@pass_context
def update_receipt(ctx: Context, id: str, **kwargs: str | None) -> None:
    """Update a receipt by ID."""
    client = ctx.get_client()
    doc = {k: v for k, v in kwargs.items() if v is not None}
    data = client.patch(f"documents/receipts/{id}", json={"receipt": doc})
    echo_output(data, fmt=ctx.output_format)


# --- Typeless Documents ---

@click.group(name="typeless-documents")
def typeless_documents() -> None:
    """Manage typeless documents (unclassified uploads)."""

typeless_documents.add_command(_list_cmd("documents/typeless_documents", ["id", "contact_id", "reference", "date", "state"]))
typeless_documents.add_command(_get_cmd("documents/typeless_documents"))
typeless_documents.add_command(_delete_cmd("documents/typeless_documents"))

@typeless_documents.command("create")
@click.option("--contact-id", help="Contact ID.")
@click.option("--reference", help="Document reference.")
@pass_context
def create_typeless_document(ctx: Context, **kwargs: str | None) -> None:
    """Create a new typeless document."""
    client = ctx.get_client()
    doc = {k: v for k, v in kwargs.items() if v is not None}
    data = client.post("documents/typeless_documents", json={"typeless_document": doc})
    echo_output(data, fmt=ctx.output_format)
