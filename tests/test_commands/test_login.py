"""Tests for login/logout commands."""

import responses

from moneybird_cli.client import API_BASE
from moneybird_cli.config import load_config


def test_login_with_explicit_id(cli_runner):
    result = cli_runner("login", "--token", "my-token", "--administration-id", "12345")
    assert result.exit_code == 0
    assert "Logged in" in result.output

    config = load_config(cli_runner.config_path)
    assert config["administrations"]["default"]["token"] == "my-token"
    assert config["administrations"]["default"]["administration_id"] == "12345"


@responses.activate
def test_login_auto_detect_single_administration(cli_runner):
    responses.add(
        responses.GET,
        f"{API_BASE}/administrations.json",
        json=[{"id": 42, "name": "My Company"}],
    )
    result = cli_runner("login", "--token", "my-token")
    assert result.exit_code == 0
    assert "Auto-detected" in result.output
    assert "My Company" in result.output
    assert "Logged in" in result.output

    config = load_config(cli_runner.config_path)
    assert config["administrations"]["default"]["administration_id"] == "42"


@responses.activate
def test_login_multiple_administrations_errors(cli_runner):
    responses.add(
        responses.GET,
        f"{API_BASE}/administrations.json",
        json=[
            {"id": 1, "name": "Company A"},
            {"id": 2, "name": "Company B"},
        ],
    )
    result = cli_runner("login", "--token", "my-token")
    assert result.exit_code != 0
    assert "Multiple administrations" in result.output
    assert "--administration-id" in result.output
    assert "Company A" in result.output
    assert "Company B" in result.output


@responses.activate
def test_login_no_administrations_errors(cli_runner):
    responses.add(
        responses.GET,
        f"{API_BASE}/administrations.json",
        json=[],
    )
    result = cli_runner("login", "--token", "my-token")
    assert result.exit_code != 0
    assert "No administrations" in result.output


def test_login_named_administration(runner, tmp_path):
    from moneybird_cli.main import cli

    config_path = tmp_path / "config.toml"
    result = runner.invoke(
        cli,
        [
            "--config", str(config_path),
            "--administration", "my-company",
            "login",
            "--token", "tok",
            "--administration-id", "999",
        ],
    )
    assert result.exit_code == 0
    config = load_config(config_path)
    assert "my-company" in config["administrations"]


def test_logout(cli_runner):
    cli_runner("login", "--token", "tok", "--administration-id", "123")
    result = cli_runner("logout")
    assert result.exit_code == 0
    assert "Logged out" in result.output

    config = load_config(cli_runner.config_path)
    assert "default" not in config.get("administrations", {})
