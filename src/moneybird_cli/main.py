"""Moneybird CLI - main entry point and global options."""

from __future__ import annotations

import time
from pathlib import Path

import click


def _default_timezone() -> str:
    """Return the system's local IANA timezone name (e.g., Europe/Amsterdam)."""
    import os
    # 1. Explicit TZ env var
    tz = os.environ.get("TZ")
    if tz and "/" in tz:
        return tz
    # 2. /etc/timezone (Debian/Ubuntu)
    try:
        return Path("/etc/timezone").read_text().strip()
    except OSError:
        pass
    # 3. /etc/localtime symlink (most Linux, macOS)
    try:
        return os.readlink("/etc/localtime").split("zoneinfo/")[-1]
    except OSError:
        pass
    # 4. Abbreviation fallback
    return time.tzname[0]

from moneybird_cli.client import MoneybirdClient
from moneybird_cli.config import (
    DEFAULT_CONFIG_PATH,
    complete_administration,
    get_administration,
    load_config,
)


class Context:
    """Shared context for all commands."""

    def __init__(self) -> None:
        self.verbose: bool = False
        self.quiet: bool = False
        self.output_format: str = "auto"
        self.no_color: bool = False
        self.dry_run: bool = False
        self.timezone: str = _default_timezone()
        self.config_path: Path = DEFAULT_CONFIG_PATH
        self.administration_name: str | None = None
        self.token: str | None = None
        self.administration_id: str | None = None

    def get_client(self) -> MoneybirdClient:
        """Build a MoneybirdClient from config/options."""
        token = self.token
        administration_id = self.administration_id

        if not token or not administration_id:
            config = load_config(self.config_path)
            admin = get_administration(config, self.administration_name)
            token = token or admin.get("token")
            administration_id = administration_id or admin.get("administration_id")

        if not token:
            raise click.ClickException(
                "No API token configured. Run 'moneybird login' or use --token."
            )
        if not administration_id:
            raise click.ClickException(
                "No administration ID configured. Run 'moneybird login' or use --administration-id."
            )

        return MoneybirdClient(
            token=token,
            administration_id=administration_id,
            dry_run=self.dry_run,
            verbose=self.verbose,
            timezone=self.timezone,
        )


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.version_option(package_name="moneybird-cli", prog_name="moneybird")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output.")
@click.option("-q", "--quiet", is_flag=True, help="Suppress all output except errors.")
@click.option(
    "--administration",
    metavar="NAME",
    shell_complete=complete_administration,
    help="Administration name to use (from config).",
)
@click.option("--token", metavar="TOKEN", help="API token for authentication.")
@click.option(
    "--administration-id", metavar="ID", help="Moneybird administration ID."
)
@click.option(
    "--output",
    "output_format",
    type=click.Choice(["auto", "json", "table"]),
    default="auto",
    help="Output format.",
)
@click.option("--no-color", is_flag=True, help="Disable colored output.")
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path),
    default=None,
    help="Custom config file path.",
)
@click.option("--dry-run", is_flag=True, help="Show actions without executing them.")
@click.option("--timezone", "timezone", default=None, metavar="TZ", help="IANA timezone for API requests (e.g., Europe/Amsterdam). Defaults to system timezone.")
@pass_context
def cli(
    ctx: Context,
    verbose: bool,
    quiet: bool,
    administration: str | None,
    token: str | None,
    administration_id: str | None,
    output_format: str,
    no_color: bool,
    config_path: Path | None,
    dry_run: bool,
    timezone: str | None,
) -> None:
    """Moneybird CLI - interact with the Moneybird API from your terminal."""
    ctx.verbose = verbose
    ctx.quiet = quiet
    ctx.output_format = output_format
    ctx.no_color = no_color
    ctx.dry_run = dry_run
    ctx.administration_name = administration
    ctx.token = token
    ctx.administration_id = administration_id
    if config_path:
        ctx.config_path = config_path
    if timezone:
        ctx.timezone = timezone


@cli.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell: str) -> None:
    """Print the shell completion script for SHELL.

    \b
    bash: moneybird completion bash > ~/.local/share/bash-completion/completions/moneybird
    zsh:  moneybird completion zsh > "${fpath[1]}/_moneybird"
    fish: moneybird completion fish > ~/.config/fish/completions/moneybird.fish
    """
    from click.shell_completion import get_completion_class

    comp_cls = get_completion_class(shell)
    click.echo(comp_cls(cli, {}, "moneybird", "_MONEYBIRD_COMPLETE").source())


# Register command groups
from moneybird_cli.commands.login import login, logout, set_default  # noqa: E402
from moneybird_cli.commands.contacts import contacts  # noqa: E402
from moneybird_cli.commands.products import products  # noqa: E402
from moneybird_cli.commands.sales_invoices import sales_invoices  # noqa: E402
from moneybird_cli.commands.estimates import estimates  # noqa: E402
from moneybird_cli.commands.ledger_accounts import ledger_accounts  # noqa: E402
from moneybird_cli.commands.projects import projects  # noqa: E402
from moneybird_cli.commands.time_entries import time_entries  # noqa: E402
from moneybird_cli.commands.financial_accounts import financial_accounts  # noqa: E402
from moneybird_cli.commands.financial_mutations import financial_mutations  # noqa: E402
from moneybird_cli.commands.financial_statements import financial_statements  # noqa: E402
from moneybird_cli.commands.payments import payments  # noqa: E402
from moneybird_cli.commands.reports import reports  # noqa: E402
from moneybird_cli.commands.documents import (  # noqa: E402
    general_documents,
    general_journal_documents,
    purchase_invoices,
    receipts,
    typeless_documents,
)
from moneybird_cli.commands.external_sales_invoices import external_sales_invoices  # noqa: E402
from moneybird_cli.commands.assets import assets  # noqa: E402
from moneybird_cli.commands.purchase_transactions import purchase_transactions  # noqa: E402
from moneybird_cli.commands.recurring_sales_invoices import recurring_sales_invoices  # noqa: E402
from moneybird_cli.commands.subscriptions import subscriptions  # noqa: E402
from moneybird_cli.commands.tax_rates import tax_rates  # noqa: E402
from moneybird_cli.commands.task_lists import task_lists  # noqa: E402
from moneybird_cli.commands.administration import (  # noqa: E402
    custom_fields,
    document_styles,
    downloads,
    identities,
    users,
    verifications,
    workflows,
)
from moneybird_cli.commands.webhooks import webhooks  # noqa: E402

cli.add_command(login)
cli.add_command(logout)
cli.add_command(set_default)
cli.add_command(contacts)
cli.add_command(products)
cli.add_command(sales_invoices)
cli.add_command(estimates)
cli.add_command(ledger_accounts)
cli.add_command(projects)
cli.add_command(time_entries)
cli.add_command(financial_accounts)
cli.add_command(financial_mutations)
cli.add_command(financial_statements)
cli.add_command(payments)
cli.add_command(reports)
cli.add_command(general_documents)
cli.add_command(general_journal_documents, name="journal-documents")
cli.add_command(purchase_invoices)
cli.add_command(receipts)
cli.add_command(typeless_documents)
cli.add_command(external_sales_invoices)
cli.add_command(assets)
cli.add_command(purchase_transactions)
cli.add_command(recurring_sales_invoices)
cli.add_command(subscriptions)
cli.add_command(tax_rates)
cli.add_command(task_lists)
cli.add_command(custom_fields)
cli.add_command(document_styles)
cli.add_command(downloads)
cli.add_command(identities)
cli.add_command(users)
cli.add_command(verifications)
cli.add_command(workflows)
cli.add_command(webhooks)
