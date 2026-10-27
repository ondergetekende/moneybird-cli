"""Sub-commands shared by several resources (notes, attachments, payments, ...)."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output
from moneybird_cli.client import MoneybirdClient


def clean(kwargs: dict) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


def save_download(ctx: Context, client: MoneybirdClient, path: str, output: str, method: str = "GET") -> None:
    content = client.download(path, method=method)
    with open(output, "wb") as f:
        f.write(content)
    if not ctx.quiet:
        click.echo(f"Saved to {output}")


def add_sync(group: click.Group, base: str, columns: list[str] | None = None) -> None:
    @group.command("sync")
    @click.option("--filter", "filter_", help="Filter terms, e.g. 'period:this_year,state:all'.")
    @pass_context
    def sync(ctx: Context, filter_: str | None) -> None:
        """Fetch all records via the synchronization API (not limited by pagination)."""
        data = ctx.get_client().sync_all(base, params=clean({"filter": filter_}))
        echo_output(data, fmt=ctx.output_format, columns=columns)


def add_notes(group: click.Group, base: str) -> None:
    @group.command("note")
    @click.argument("id")
    @click.argument("note")
    @click.option("--todo", is_flag=True, default=None, help="Mark the note as a to-do.")
    @click.option("--assignee-id", help="User ID to assign the to-do to.")
    @pass_context
    def note(ctx: Context, id: str, **kwargs: str | bool | None) -> None:
        """Add a note to a record."""
        data = ctx.get_client().post(f"{base}/{id}/notes", json={"note": clean(kwargs)})
        echo_output(data, fmt=ctx.output_format)

    @group.command("delete-note")
    @click.argument("id")
    @click.argument("note_id")
    @pass_context
    def delete_note(ctx: Context, id: str, note_id: str) -> None:
        """Delete a note from a record."""
        ctx.get_client().delete(f"{base}/{id}/notes/{note_id}")
        if not ctx.quiet:
            click.echo(f"Note {note_id} deleted.")


def add_attachments(group: click.Group, base: str, upload: str = "attachments") -> None:
    @group.command("attach")
    @click.argument("id")
    @click.argument("file", type=click.Path(exists=True, dir_okay=False))
    @pass_context
    def attach(ctx: Context, id: str, file: str) -> None:
        """Upload a file as attachment."""
        ctx.get_client().upload(f"{base}/{id}/{upload}", file)
        if not ctx.quiet:
            click.echo(f"Attached {file}.")

    @group.command("download-attachment")
    @click.argument("id")
    @click.argument("attachment_id")
    @click.option("--output", "output_path", type=click.Path(), required=True, help="Output file path.")
    @pass_context
    def download_attachment(ctx: Context, id: str, attachment_id: str, output_path: str) -> None:
        """Download an attachment."""
        save_download(ctx, ctx.get_client(), f"{base}/{id}/attachments/{attachment_id}/download", output_path)

    @group.command("delete-attachment")
    @click.argument("id")
    @click.argument("attachment_id")
    @pass_context
    def delete_attachment(ctx: Context, id: str, attachment_id: str) -> None:
        """Delete an attachment."""
        ctx.get_client().delete(f"{base}/{id}/attachments/{attachment_id}")
        if not ctx.quiet:
            click.echo(f"Attachment {attachment_id} deleted.")


def add_payments(group: click.Group, base: str) -> None:
    @group.command("pay")
    @click.argument("id")
    @click.option("--amount", "price", required=True, help="Payment amount.")
    @click.option("--date", "payment_date", required=True, help="Payment date (YYYY-MM-DD).")
    @click.option("--financial-account-id", help="Financial account ID.")
    @click.option("--financial-mutation-id", help="Financial mutation (bank transaction) ID.")
    @click.option("--ledger-account-id", help="Ledger account ID.")
    @click.option("--transaction-identifier", help="Transaction identifier.")
    @click.option("--manual-payment-action", help="Manual payment action (e.g., private_payment, payment_without_proof).")
    @pass_context
    def pay(ctx: Context, id: str, **kwargs: str | None) -> None:
        """Register a payment."""
        data = ctx.get_client().post(f"{base}/{id}/payments", json={"payment": clean(kwargs)})
        echo_output(data, fmt=ctx.output_format)

    @group.command("delete-payment")
    @click.argument("id")
    @click.argument("payment_id")
    @pass_context
    def delete_payment(ctx: Context, id: str, payment_id: str) -> None:
        """Delete a payment."""
        ctx.get_client().delete(f"{base}/{id}/payments/{payment_id}")
        if not ctx.quiet:
            click.echo(f"Payment {payment_id} deleted.")


def add_collection_states(group: click.Group, base: str) -> None:
    @group.command("mark-dubious")
    @click.argument("id")
    @click.option("--date", "dubious_date", help="Date (YYYY-MM-DD).")
    @pass_context
    def mark_dubious(ctx: Context, id: str, dubious_date: str | None) -> None:
        """Mark as dubious (doubtful debt)."""
        data = ctx.get_client().patch(f"{base}/{id}/mark_as_dubious", json=clean({"dubious_date": dubious_date}))
        echo_output(data, fmt=ctx.output_format)

    @group.command("mark-uncollectible")
    @click.argument("id")
    @click.option("--date", "uncollectible_date", help="Date (YYYY-MM-DD).")
    @click.option("--book-method", help="Booking method (e.g., revenue).")
    @pass_context
    def mark_uncollectible(ctx: Context, id: str, **kwargs: str | None) -> None:
        """Mark as uncollectible."""
        data = ctx.get_client().patch(f"{base}/{id}/mark_as_uncollectible", json=clean(kwargs))
        echo_output(data, fmt=ctx.output_format)


def add_additional_charges(group: click.Group, base: str) -> None:
    @group.command("charges")
    @click.argument("id")
    @click.option("--include-billed", is_flag=True, default=None, help="Include already billed charges.")
    @pass_context
    def charges(ctx: Context, id: str, include_billed: bool | None) -> None:
        """List additional charges."""
        data = ctx.get_client().get(f"{base}/{id}/additional_charges", params=clean({"include_billed": include_billed}))
        echo_output(data, fmt=ctx.output_format)

    @group.command("add-charge")
    @click.argument("id")
    @click.option("--product-id", required=True, help="Product ID.")
    @click.option("--amount", help="Amount, e.g. '5 x'.")
    @click.option("--price", help="Price per unit.")
    @click.option("--period", help="Period, e.g. 20240601..20240630.")
    @click.option("--description", help="Description.")
    @pass_context
    def add_charge(ctx: Context, id: str, **kwargs: str | None) -> None:
        """Add a charge to be invoiced with the next period."""
        data = ctx.get_client().post(f"{base}/{id}/additional_charges", json=clean(kwargs))
        echo_output(data, fmt=ctx.output_format)
