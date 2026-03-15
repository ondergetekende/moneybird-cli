"""Moneybird CLI - main entry point and global options."""

from __future__ import annotations

from pathlib import Path

import click

from moneybird_cli.client import MoneybirdClient
from moneybird_cli.config import (
    DEFAULT_CONFIG_PATH,
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
        )


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.version_option(version="0.1.0", prog_name="moneybird")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output.")
@click.option("-q", "--quiet", is_flag=True, help="Suppress all output except errors.")
@click.option(
    "--administration",
    metavar="NAME",
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


# Register command groups
from moneybird_cli.commands.login import login, logout  # noqa: E402
from moneybird_cli.commands.contacts import contacts  # noqa: E402
from moneybird_cli.commands.products import products  # noqa: E402
from moneybird_cli.commands.sales_invoices import sales_invoices  # noqa: E402
from moneybird_cli.commands.estimates import estimates  # noqa: E402
from moneybird_cli.commands.ledger_accounts import ledger_accounts  # noqa: E402

cli.add_command(login)
cli.add_command(logout)
cli.add_command(contacts)
cli.add_command(products)
cli.add_command(sales_invoices)
cli.add_command(estimates)
cli.add_command(ledger_accounts)
