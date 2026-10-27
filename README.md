# Moneybird CLI

A command-line interface for [Moneybird](https://www.moneybird.com/), the online accounting platform. Manage invoices, contacts, expenses, time tracking, and more from your terminal.

> **Disclaimer:** This project is not affiliated with, endorsed by, or in any way associated with Moneybird B.V. "Moneybird" is a trademark of Moneybird B.V. This is an independent, open-source tool that uses the public Moneybird API.

## Quick start

```bash
pip install moneybird-cli
moneybird login --token YOUR_API_TOKEN
moneybird contacts list
moneybird sales-invoices list --state open
```

See [Getting Started](docs/getting-started.md) for full setup instructions, output formats, pagination, and global options.

## Documentation

| Guide | What it covers |
| --- | --- |
| [Getting Started](docs/getting-started.md) | Installation, authentication, multiple administrations, output formats, pagination, global options |
| [Contacts](docs/contacts.md) | Customer and supplier management: list, search, filter, create, update, archive |
| [Invoicing](docs/invoicing.md) | Sales invoices, estimates, recurring invoices, external invoices, payments, credit notes, PDF downloads |
| [Products & Subscriptions](docs/products-and-subscriptions.md) | Reusable product definitions, subscription lifecycle management |
| [Financial](docs/financial.md) | Bank accounts, transactions, reconciliation, purchase transactions |
| [Documents](docs/documents.md) | Purchase invoices, receipts, journal entries, general documents, assets |
| [Time Tracking](docs/time-tracking.md) | Projects and time entries |
| [Reports](docs/reports.md) | Profit/loss, balance sheet, cash flow, tax, debtors/creditors, and more |
| [Settings](docs/settings.md) | Ledger accounts, tax rates, webhooks, task lists |

## Tech stack

- [Python](https://www.python.org/) >= 3.11
- [Click](https://click.palletsprojects.com/) for the CLI framework
- [Requests](https://requests.readthedocs.io/) for HTTP
- [Tabulate](https://pypi.org/project/tabulate/) for table formatting

## License

MIT -- see [LICENSE](LICENSE).
