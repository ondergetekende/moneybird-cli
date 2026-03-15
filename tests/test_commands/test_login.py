"""Tests for login/logout commands."""

from moneybird_cli.config import load_config


def test_login(cli_runner):
    result = cli_runner("login", "--token", "my-token", "--administration-id", "12345")
    assert result.exit_code == 0
    assert "Logged in" in result.output

    config = load_config(cli_runner.config_path)
    assert config["administrations"]["default"]["token"] == "my-token"
    assert config["administrations"]["default"]["administration_id"] == "12345"


def test_login_named_administration(runner, tmp_path):
    from click.testing import CliRunner
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
