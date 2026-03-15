# Moneybird CLI

This is a command-line interface (CLI) for interacting with the Moneybird API. It allows you to perform various operations such as creating invoices, managing contacts, and more, directly from your terminal.

> **Disclaimer:** This project is not affiliated with, endorsed by, or in any way associated with Moneybird B.V. "Moneybird" is a trademark of Moneybird B.V. This is an independent, open-source tool that uses the public Moneybird API.

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

### Projects

- `moneybird projects list [--all] [--state active|archived|all]`: List projects.
- `moneybird projects get <ID>`: Get a single project.
- `moneybird projects create --name NAME [--budget ...]`: Create a project.
- `moneybird projects update <ID> [--name ...]`: Update a project.
- `moneybird projects delete <ID>`: Delete a project.

### Time Entries

- `moneybird time-entries list [--all] [--state STATE] [--period PERIOD] [--project-id ID]`: List time entries.
- `moneybird time-entries get <ID>`: Get a single time entry.
- `moneybird time-entries create --started-at TIME --ended-at TIME [--description ...]`: Create a time entry.
- `moneybird time-entries update <ID> [--description ...]`: Update a time entry.
- `moneybird time-entries delete <ID>`: Delete a time entry.

### Recurring Sales Invoices

- `moneybird recurring-sales-invoices list [--all]`: List recurring invoices.
- `moneybird recurring-sales-invoices get <ID>`: Get a single recurring invoice.
- `moneybird recurring-sales-invoices create --contact-id ID --frequency-type TYPE --frequency N`: Create a recurring invoice.
- `moneybird recurring-sales-invoices update <ID> [--frequency ...]`: Update a recurring invoice.
- `moneybird recurring-sales-invoices delete <ID>`: Delete a recurring invoice.

### Subscriptions

- `moneybird subscriptions list [--all]`: List subscriptions.
- `moneybird subscriptions get <ID>`: Get a single subscription.
- `moneybird subscriptions create --contact-id ID [--product-id ID ...]`: Create a subscription.
- `moneybird subscriptions update <ID> [--product-id ...]`: Update a subscription.
- `moneybird subscriptions cancel <ID>`: Cancel a subscription.

### Financial Accounts

- `moneybird financial-accounts list`: List all financial accounts (bank accounts, credit cards, etc.).

### Financial Mutations

- `moneybird financial-mutations list [--all] [--state STATE] [--period PERIOD] [--mutation-type TYPE]`: List financial mutations.
- `moneybird financial-mutations get <ID>`: Get a single financial mutation.
- `moneybird financial-mutations link <ID> --booking-type TYPE --booking-id ID`: Link a mutation to a booking.
- `moneybird financial-mutations unlink <ID> --booking-type TYPE --booking-id ID`: Unlink a booking.

### Financial Statements

- `moneybird financial-statements create --financial-account-id ID --reference REF`: Create a financial statement.
- `moneybird financial-statements update <ID> [--reference ...]`: Update a financial statement.
- `moneybird financial-statements delete <ID>`: Delete a financial statement.

### Documents

General documents, journal documents, purchase invoices, receipts, and typeless documents all share the same command structure:

- `moneybird <type> list [--all] [--period PERIOD]`: List documents.
- `moneybird <type> get <ID>`: Get a single document.
- `moneybird <type> create [--contact-id ID] [--reference ...]`: Create a document.
- `moneybird <type> update <ID> [--reference ...]`: Update a document.
- `moneybird <type> delete <ID>`: Delete a document.

Where `<type>` is one of: `general-documents`, `journal-documents`, `purchase-invoices`, `receipts`, `typeless-documents`.

### External Sales Invoices

- `moneybird external-sales-invoices list [--all] [--state STATE] [--period PERIOD]`: List external invoices.
- `moneybird external-sales-invoices get <ID>`: Get a single external invoice.
- `moneybird external-sales-invoices create --contact-id ID [--reference ...]`: Create an external invoice.
- `moneybird external-sales-invoices update <ID> [--reference ...]`: Update an external invoice.
- `moneybird external-sales-invoices delete <ID>`: Delete an external invoice.

### Assets

- `moneybird assets list [--all] [--include-inactive] [--ledger-account-id ID]`: List assets.
- `moneybird assets get <ID>`: Get a single asset.
- `moneybird assets create --name NAME [--purchase-date DATE ...]`: Create an asset.
- `moneybird assets update <ID> [--name ...]`: Update an asset.
- `moneybird assets delete <ID>`: Delete an asset.

### Purchase Transactions

- `moneybird purchase-transactions list [--all] [--state STATE] [--period PERIOD]`: List purchase transactions.
- `moneybird purchase-transactions get <ID>`: Get a single purchase transaction.
- `moneybird purchase-transactions delete <ID>`: Delete a pending purchase transaction.

### Tax Rates

- `moneybird tax-rates list [--all]`: List tax rates.

### Payments

- `moneybird payments get <ID>`: Get a single payment.

### Reports

- `moneybird reports get <TYPE> [--period PERIOD] [--contact-id ID] [--project-id ID]`: Fetch a financial report.

Available report types: `profit_loss`, `balance_sheet`, `cash_flow`, `tax`, `debtors`, `debtors_aging`, `creditors`, `general_ledger`, `journal_entries`, `revenue_by_contact`, `revenue_by_project`, `expenses_by_contact`, `expenses_by_project`, `subscriptions`, `assets`.

### Webhooks

- `moneybird webhooks list`: List all webhooks.
- `moneybird webhooks create --url URL --events EVENT [--events EVENT ...]`: Create a webhook.
- `moneybird webhooks delete <ID>`: Delete a webhook.
- `moneybird webhooks activate <ID>`: Activate a webhook.
- `moneybird webhooks deactivate <ID>`: Deactivate a webhook.

### Pagination

All `list` commands return the first page by default. Use `--all` to auto-paginate through all results (respects API rate limits). Use `--page N` to fetch a specific page, and `--per-page N` to control page size (max 100).
