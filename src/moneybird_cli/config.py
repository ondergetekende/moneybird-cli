"""Configuration management for Moneybird CLI."""

from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]


DEFAULT_CONFIG_PATH = Path.home() / ".config" / "moneybird-cli.toml"


def _serialize_toml(data: dict, prefix: str = "") -> str:
    """Serialize a dict to TOML format (minimal implementation)."""
    lines: list[str] = []
    # Write scalar keys first
    for key, value in data.items():
        if not isinstance(value, dict):
            lines.append(f"{key} = {_toml_value(value)}")
    # Write tables (possibly nested)
    for key, value in data.items():
        if isinstance(value, dict):
            full_key = f"{prefix}.{key}" if prefix else key
            # Check if this dict has nested dicts (sub-tables)
            has_subtables = any(isinstance(v, dict) for v in value.values())
            if has_subtables:
                # Write scalar keys under this table header
                scalars = {k: v for k, v in value.items() if not isinstance(v, dict)}
                if scalars:
                    lines.append("")
                    lines.append(f"[{full_key}]")
                    for k, v in scalars.items():
                        lines.append(f"{k} = {_toml_value(v)}")
                # Recurse for sub-tables
                subtables = {k: v for k, v in value.items() if isinstance(v, dict)}
                lines.append(_serialize_toml(subtables, prefix=full_key))
            else:
                lines.append("")
                lines.append(f"[{full_key}]")
                for k, v in value.items():
                    lines.append(f"{k} = {_toml_value(v)}")
    return "\n".join(lines)


def _toml_value(value: object) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    raise TypeError(f"Unsupported TOML value type: {type(value)}")


def load_config(path: Path | None = None) -> dict:
    """Load configuration from TOML file."""
    config_path = path or DEFAULT_CONFIG_PATH
    if not config_path.exists():
        return {}
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def save_config(data: dict, path: Path | None = None) -> None:
    """Save configuration to TOML file."""
    config_path = path or DEFAULT_CONFIG_PATH
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(_serialize_toml(data) + "\n")


def get_administration(config: dict, name: str | None = None) -> dict:
    """Get credentials for a named administration.

    If name is None, returns the default administration.
    """
    if name is None:
        name = config.get("default_administration", "default")
    admins = config.get("administrations", {})
    return admins.get(name, {})


def set_administration(
    config: dict,
    token: str,
    administration_id: str,
    name: str | None = None,
) -> dict:
    """Set credentials for a named administration."""
    if name is None:
        name = "default"
    if "administrations" not in config:
        config["administrations"] = {}
    config["administrations"][name] = {
        "token": token,
        "administration_id": administration_id,
    }
    if "default_administration" not in config:
        config["default_administration"] = name
    return config


def remove_administration(config: dict, name: str | None = None) -> dict:
    """Remove credentials for a named administration."""
    if name is None:
        name = config.get("default_administration", "default")
    admins = config.get("administrations", {})
    admins.pop(name, None)
    if config.get("default_administration") == name:
        # Set new default or remove
        if admins:
            config["default_administration"] = next(iter(admins))
        else:
            config.pop("default_administration", None)
    return config
