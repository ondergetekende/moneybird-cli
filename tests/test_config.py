"""Tests for config module."""

from moneybird_cli.config import (
    get_administration,
    load_config,
    remove_administration,
    save_config,
    set_administration,
)


def test_load_nonexistent_config(tmp_path):
    path = tmp_path / "nonexistent.toml"
    assert load_config(path) == {}


def test_save_and_load_config(tmp_path):
    path = tmp_path / "config.toml"
    config = set_administration({}, "my-token", "12345", "default")
    save_config(config, path)
    loaded = load_config(path)
    assert loaded["administrations"]["default"]["token"] == "my-token"
    assert loaded["administrations"]["default"]["administration_id"] == "12345"


def test_save_config_restricts_permissions(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text("")
    path.chmod(0o644)
    save_config({}, path)
    assert path.stat().st_mode & 0o777 == 0o600


def test_multiple_administrations(tmp_path):
    path = tmp_path / "config.toml"
    config = set_administration({}, "token-a", "111", "company-a")
    config = set_administration(config, "token-b", "222", "company-b")
    save_config(config, path)
    loaded = load_config(path)
    assert get_administration(loaded, "company-a")["token"] == "token-a"
    assert get_administration(loaded, "company-b")["token"] == "token-b"


def test_default_administration():
    config = set_administration({}, "tok", "999")
    assert config["default_administration"] == "default"
    admin = get_administration(config)
    assert admin["token"] == "tok"


def test_remove_administration():
    config = set_administration({}, "tok", "999", "test")
    config = remove_administration(config, "test")
    assert "test" not in config.get("administrations", {})


def test_remove_default_switches():
    config = set_administration({}, "tok1", "111", "a")
    config = set_administration(config, "tok2", "222", "b")
    config["default_administration"] = "a"
    config = remove_administration(config, "a")
    assert config["default_administration"] == "b"
