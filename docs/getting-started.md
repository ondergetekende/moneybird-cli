# Getting Started

## What is Moneybird?

[Moneybird](https://www.moneybird.com/) is a Dutch online accounting platform popular with freelancers and small businesses. It handles invoicing, expense tracking, time registration, and financial reporting.

This CLI lets you interact with your Moneybird administration from the terminal -- useful for scripting, automation, and quick lookups without opening a browser.

## Installation

```bash
pip install moneybird-cli
```

This installs a `moneybird` command in your PATH.

### Shell completion

Generate a completion script for your shell and install it:

```bash
# bash
moneybird completion bash > ~/.local/share/bash-completion/completions/moneybird
# zsh (pick a directory in your $fpath)
moneybird completion zsh > "${fpath[1]}/_moneybird"
# fish
moneybird completion fish > ~/.config/fish/completions/moneybird.fish
```

Restart your shell afterwards. Administration names from your config are completed too.

## Authentication

You need a personal API token from Moneybird:

1. Log in at [moneybird.com](https://www.moneybird.com/).
2. Go to **Settings** > **API** (in the sidebar under "Developer").
3. Generate a new personal access token and copy it.

Then tell the CLI about it:

```bash
moneybird login --token YOUR_API_TOKEN
```

If your account has access to a single administration (company/bookkeeping), the CLI auto-detects it. If you have multiple, it will list them and ask you to pick one:

```bash
moneybird login --token YOUR_API_TOKEN --administration-id 123456789
```

Credentials are stored in `~/.config/moneybird-cli.toml`.

## Multiple administrations

If you manage books for more than one company, you can store credentials for each under a name:

```bash
moneybird --administration "acme-corp" login --token TOKEN_A --administration-id 111
moneybird --administration "side-project" login --token TOKEN_B --administration-id 222
```

Switch the default with:

```bash
moneybird default acme-corp
```

Or pass `--administration NAME` to any command to use a specific one for that call.

## Output formats

By default the CLI prints tables when you're in a terminal, and JSON when output is piped:

```bash
# Human-readable table
moneybird contacts list

# JSON for scripting
moneybird contacts list | jq '.[].company_name'

# Force a format
moneybird contacts list --output json
moneybird contacts list --output table
```

## Pagination

All `list` commands return the first page of results by default (up to 100 items). To fetch everything:

```bash
moneybird contacts list --all
```

Or navigate manually:

```bash
moneybird contacts list --page 2 --per-page 50
```

The `--all` flag respects Moneybird's rate limits (150 requests per 5 minutes) and automatically pauses when the limit is nearly exhausted.

Resources with a synchronization API (contacts, sales/external/recurring invoices, estimates, and all document types) also have a `sync` command, which fetches every record by ID instead of page by page, and accepts the same `--filter` terms as the API:

```bash
moneybird sales-invoices sync --filter period:this_year,state:all
```

## Timezone

The CLI sends your system timezone to Moneybird with every request, so dates and times are returned in your local timezone. Override it with:

```bash
moneybird --timezone America/New_York sales-invoices list
```

## Dry run

To see what API calls a command would make without actually executing them:

```bash
moneybird --dry-run sales-invoices create --contact-id 123
```

This prints the HTTP method and URL but doesn't create anything. Read operations (list, get) still execute normally.

## Global options

These can be used with any command:

| Option | Description |
|---|---|
| `--help` | Show help for a command |
| `--version` | Show version |
| `-v, --verbose` | Print HTTP requests to stderr |
| `-q, --quiet` | Suppress non-error output |
| `--administration NAME` | Use a specific named administration |
| `--token TOKEN` | Override the stored API token |
| `--administration-id ID` | Override the stored administration ID |
| `--output auto\|json\|table` | Force output format |
| `--no-color` | Disable colored output |
| `--config PATH` | Use a custom config file |
| `--dry-run` | Show write actions without executing them |
| `--timezone TZ` | Override the timezone sent to the API |
