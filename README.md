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
moneybird login --token YOUR_API_TOKEN
```

If you have a single administration, the CLI will automatically detect its ID. If you have multiple administrations, you will be prompted to specify one:

```bash
moneybird login --token YOUR_API_TOKEN --administration-id YOUR_ADMINISTRATION_ID
```

If you wish to deal with multiple administrations, you can specify a name for each:

```bash
moneybird --administration "my-company" login --token YOUR_API_TOKEN --administration-id YOUR_ADMINISTRATION_ID
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

### Authentication

- `moneybird login --token TOKEN [--administration-id ID]`: Log in by saving API credentials. Auto-detects administration ID if you have exactly one.
- `moneybird logout`: Log out and clear stored credentials.
- `moneybird default <NAME>`: Set the default administration (when multiple are configured).

### Contacts

- `moneybird contacts list [--all] [--page N] [--per-page N] [--include-archived]`: List contacts (first page by default, `--all` to fetch everything).
- `moneybird contacts get <ID>`: Get a single contact.
- `moneybird contacts search <QUERY>`: Search contacts by name or email.
- `moneybird contacts filter [--created-after DATE] [--updated-after DATE]`: Filter contacts.
- `moneybird contacts create --company-name NAME [--email ...]`: Create a contact.
- `moneybird contacts update <ID> [--company-name ...]`: Update a contact.
- `moneybird contacts delete <ID>`: Delete a contact.
- `moneybird contacts archive <ID>`: Archive a contact.

### Sales Invoices

- `moneybird sales-invoices list [--all] [--state STATE] [--contact-id ID]`: List invoices.
- `moneybird sales-invoices get <ID>`: Get a single invoice.
- `moneybird sales-invoices find <INVOICE_ID>`: Find by invoice ID.
- `moneybird sales-invoices create --contact-id ID [--invoice-date DATE ...]`: Create an invoice.
- `moneybird sales-invoices update <ID> [--invoice-date ...]`: Update an invoice.
- `moneybird sales-invoices delete <ID>`: Delete an invoice.
- `moneybird sales-invoices send <ID> [--delivery-method Email]`: Send an invoice.
- `moneybird sales-invoices pay <ID> --amount AMT --date DATE`: Register a payment.
- `moneybird sales-invoices pdf <ID> [--output FILE]`: Download invoice as PDF.
- `moneybird sales-invoices credit <ID>`: Create a credit invoice.

### Products

- `moneybird products list [--all] [--query NAME]`: List products.
- `moneybird products get <ID>`: Get a single product.
- `moneybird products find <IDENTIFIER>`: Find by product identifier/SKU.
- `moneybird products create --title TITLE [--price ...]`: Create a product.
- `moneybird products update <ID> [--title ...]`: Update a product.
- `moneybird products delete <ID>`: Delete a product.

### Estimates

- `moneybird estimates list [--all]`: List estimates.
- `moneybird estimates get <ID>`: Get a single estimate.
- `moneybird estimates create --contact-id ID [--estimate-date ...]`: Create an estimate.
- `moneybird estimates update <ID> [--estimate-date ...]`: Update an estimate.
- `moneybird estimates delete <ID>`: Delete an estimate.
- `moneybird estimates send <ID> [--delivery-method Email]`: Send an estimate.

### Ledger Accounts

- `moneybird ledger-accounts list [--all]`: List ledger accounts.
- `moneybird ledger-accounts get <ID>`: Get a single ledger account.
- `moneybird ledger-accounts create --name NAME --account-type TYPE`: Create a ledger account.
- `moneybird ledger-accounts update <ID> [--name ...]`: Update a ledger account.
- `moneybird ledger-accounts delete <ID>`: Delete a ledger account.

### Pagination

All `list` commands return the first page by default. Use `--all` to auto-paginate through all results (respects API rate limits). Use `--page N` to fetch a specific page, and `--per-page N` to control page size (max 100).
