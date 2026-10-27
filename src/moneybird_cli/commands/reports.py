"""Reports commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

REPORT_TYPES = [
    "profit_loss",
    "balance_sheet",
    "bank_balance",
    "cash_flow",
    "working_capital",
    "tax",
    "debtors",
    "debtors_aging",
    "creditors",
    "creditors_aging",
    "general_ledger",
    "journal_entries",
    "revenue_by_contact",
    "revenue_by_project",
    "expenses_by_contact",
    "expenses_by_project",
    "subscriptions",
    "assets",
]


@click.group()
def reports() -> None:
    """View financial reports."""


@reports.command("get")
@click.argument("report_type", type=click.Choice(REPORT_TYPES))
@click.option("--period", help="Period (e.g., this_month, prev_year, 202401..202412).")
@click.option("--period-until", help="End period for aging reports (e.g., this_month, 202501).")
@click.option("--granularity", type=click.Choice(["month", "quarter", "year"]), help="Split the report into periods.")
@click.option("--contact-id", help="Filter by contact ID (journal_entries).")
@click.option("--project-id", help="Filter by project ID (profit_loss, journal_entries).")
@click.option("--ledger-account-id", help="Filter by ledger account ID (journal_entries).")
@click.option("--financial-account-id", help="Filter by financial account ID (cash_flow).")
@click.option("--account-type", help="Filter by account type (journal_entries).")
@click.option("--page", type=int, help="Page number (paginated reports).")
@click.option("--per-page", type=int, help="Results per page (paginated reports).")
@pass_context
def get_report(ctx: Context, report_type: str, **kwargs: str | int | None) -> None:
    """Fetch a financial report by type. Not every option applies to every report."""
    client = ctx.get_client()
    params = {k: v for k, v in kwargs.items() if v is not None}
    data = client.get(f"reports/{report_type}", params=params)
    echo_output(data, fmt=ctx.output_format)


@reports.command("export")
@click.argument("export_type", type=click.Choice(["auditfile", "brugstaat", "ledger_accounts"]))
@click.option("--year", required=True, help="Year to export.")
@click.option("--version", type=click.Choice(["3.2", "4.0"]), help="XAF version (auditfile only).")
@pass_context
def export_report(ctx: Context, export_type: str, year: str, version: str | None) -> None:
    """Start an export. The result appears in 'moneybird downloads list' when ready."""
    body = {"year": year, **({"version": version} if version else {})}
    ctx.get_client().post(f"reports/export/{export_type}", json=body)
    if not ctx.quiet:
        click.echo("Export started; check 'moneybird downloads list'.")
