# Moneybird CLI

This is a command-line interface (CLI) for interacting with the Moneybird API. It allows you to perform various operations such as creating invoices, managing contacts, and more, directly from your terminal.

## Account setup

To use the Moneybird CLI, you need to set up your account and obtain an API token. Follow these steps:

1. Log in to your Moneybird account.
2. Navigate to the "Settings" section.
3. Click on "API" in the sidebar.
4. Generate a new API token and copy it to your clipboard.

You will also need your administration ID, which can be found in the URL when you are logged into your Moneybird account. It is the part of the URL that comes after `/administrations/` and before the next slash.

Tell the CLI about your API token by running the following command in your terminal:

```bash
moneybird login --token YOUR_API_TOKEN --administration YOUR_ADMINISTRATION_ID
```

If you wish to deal with multiple administrations, you can specify a name for each administration:

```bash
moneybird --administration "<ADMINISTRATION_NAME>" login --token YOUR_API_TOKEN --administration-id YOUR_ADMINISTRATION_ID 
```

## Global options

The Moneybird CLI supports several global options that can be used with any command:

- `--help`: Show help information for a command.
- `--version`: Show the version of the Moneybird CLI.
- `--verbose`: Enable verbose output for debugging purposes.
- `--quiet`: Suppress all output except for errors.
- `--administration <ADMINISTRATION_NAME>`: Specify the administration to use for the command.
- `--token <API_TOKEN>`: Provide the API token for authentication (if not already logged in).
- `--administration-id <ADMINISTRATION_ID>`: Provide the administration ID for authentication (if not already logged in).
- `--output <FORMAT>`: Specify the output format (e.g., json, table), default is 'auto', which uses table format for terminal output and json for non-terminal output.
- `--no-color`: Disable colored output.
- `--config <FILE_PATH>`: Specify a custom configuration file path. (Default is `~/.config/moneybird-cli.toml`).
- `--dry-run`: Show the command that would be executed without actually performing any actions.

## Commands

- `moneybird login`: Log in to your Moneybird account by providing your API token and administration ID.
- `moneybird logout`: Log out of your Moneybird account and clear stored credentials.

*TODO* Expand this section with a list of available commands and their descriptions.

## Tech stack

- [Python](https://www.python.org/) - The programming language used to develop the CLI.
- [Click](https://click.palletsprojects.com/) - A Python package for creating command-line interfaces.
- [Requests](https://requests.readthedocs.io/) - A Python library for making HTTP requests to the Moneybird API.
- [Tabulate](https://pypi.org/project/tabulate/) - A Python library for formatting tabular data in the terminal.
