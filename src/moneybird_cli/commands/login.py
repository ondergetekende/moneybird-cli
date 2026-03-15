"""Login and logout commands."""

from __future__ import annotations

from pathlib import Path

import click

from moneybird_cli.config import load_config, save_config, set_administration, remove_administration
from moneybird_cli.main import pass_context, Context


@click.command()
@click.option("--token", required=True, help="Moneybird API token.")
@click.option("--administration-id", required=True, help="Moneybird administration ID.")
@pass_context
def login(ctx: Context, token: str, administration_id: str) -> None:
    """Log in to your Moneybird account by saving API credentials."""
    config = load_config(ctx.config_path)
    config = set_administration(config, token, administration_id, ctx.administration_name)
    save_config(config, ctx.config_path)
    name = ctx.administration_name or "default"
    if not ctx.quiet:
        click.echo(f"Logged in to administration '{name}' (ID: {administration_id}).")


@click.command()
@pass_context
def logout(ctx: Context) -> None:
    """Log out by removing stored credentials."""
    config = load_config(ctx.config_path)
    name = ctx.administration_name or config.get("default_administration", "default")
    config = remove_administration(config, ctx.administration_name)
    save_config(config, ctx.config_path)
    if not ctx.quiet:
        click.echo(f"Logged out of administration '{name}'.")
