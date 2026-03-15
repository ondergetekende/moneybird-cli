"""Reports commands."""

from __future__ import annotations

import click

from moneybird_cli.main import pass_context, Context
from moneybird_cli.output import echo_output

REPORT_TYPES = [
    "profit_loss",
    "balance_sheet",
    "cash_flow",
    "tax",
    "debtors",
    "debtors_aging",
    "creditors",
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
@click.option("--period", help="Period filter (e.g., this_month, prev_year, 2024).")
@click.option("--contact-id", help="Filter by contact ID.")
@click.option("--project-id", help="Filter by project ID.")
@pass_context
def get_report(ctx: Context, report_type: str, period: str | None, contact_id: str | None, project_id: str | None) -> None:
    """Fetch a financial report by type."""
    client = ctx.get_client()
    params: dict = {}
    if period:
        params["period"] = period
    if contact_id:
        params["contact_id"] = contact_id
    if project_id:
        params["project_id"] = project_id
    data = client.get(f"reports/{report_type}", params=params)
    echo_output(data, fmt=ctx.output_format)
