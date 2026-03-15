"""Shared test fixtures."""

from __future__ import annotations

import pytest
from click.testing import CliRunner

from moneybird_cli.client import MoneybirdClient
from moneybird_cli.main import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli_runner(runner, tmp_path):
    """CLI runner with a temporary config file."""
    config_path = tmp_path / "config.toml"

    def invoke(*args, catch_exceptions=False, **kwargs):
        return runner.invoke(
            cli,
            ["--config", str(config_path), *args],
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    invoke.config_path = config_path
    return invoke


@pytest.fixture
def logged_in_runner(cli_runner):
    """CLI runner that is already logged in."""
    cli_runner("login", "--token", "test-token", "--administration-id", "123456")

    def invoke(*args, catch_exceptions=False, **kwargs):
        return cli_runner(*args, catch_exceptions=catch_exceptions, **kwargs)

    invoke.config_path = cli_runner.config_path
    return invoke
