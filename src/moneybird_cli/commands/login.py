"""Login and logout commands."""

from __future__ import annotations

from pathlib import Path

import click

from moneybird_cli.client import MoneybirdClient
from moneybird_cli.config import load_config, save_config, set_administration, remove_administration
from moneybird_cli.main import pass_context, Context


@click.command()
@click.option("--token", required=True, help="Moneybird API token.")
@click.option("--administration-id", default=None, help="Moneybird administration ID. Resolved automatically if you have exactly one.")
@pass_context
def login(ctx: Context, token: str, administration_id: str | None) -> None:
    """Log in to your Moneybird account by saving API credentials."""
    if administration_id is None:
        administrations = MoneybirdClient.list_administrations(token)
        if len(administrations) == 0:
            raise click.ClickException("No administrations found for this token.")
        if len(administrations) > 1:
            lines = ["Multiple administrations found. Use --administration-id to specify which one:", ""]
            for admin in administrations:
                lines.append(f"  {admin['id']}  {admin['name']}")
            raise click.ClickException("\n".join(lines))
        administration_id = str(administrations[0]["id"])
        if not ctx.quiet:
            click.echo(f"Auto-detected administration: {administrations[0]['name']} (ID: {administration_id})")

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


@click.command(name="default")
@click.argument("name")
@pass_context
def set_default(ctx: Context, name: str) -> None:
    """Set the default administration.

    NAME is the administration name as used during login.
    """
    config = load_config(ctx.config_path)
    admins = config.get("administrations", {})
    if name not in admins:
        available = ", ".join(sorted(admins)) if admins else "(none)"
        raise click.ClickException(f"Unknown administration '{name}'. Available: {available}")
    config["default_administration"] = name
    save_config(config, ctx.config_path)
    if not ctx.quiet:
        click.echo(f"Default administration set to '{name}'.")
