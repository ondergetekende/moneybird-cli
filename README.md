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
| [Settings](docs/settings.md) | Ledger accounts, tax rates, webhooks, task lists, identities, workflows, users |

## Tech stack

- [Python](https://www.python.org/) >= 3.8
- [Click](https://click.palletsprojects.com/) for the CLI framework
- [Requests](https://requests.readthedocs.io/) for HTTP
- [Tabulate](https://pypi.org/project/tabulate/) for table formatting

## Testing

Install tox with `python -m pip install 'tox>=4'`, then run `tox` with Python 3.8 through 3.14 available. The matrix tests minimum and current runtime dependencies on each Python version, plus minimum development dependencies and package building on Python 3.8. Run an individual environment with `tox -e py38-min`.

Keep the minimum dependency pins in `tox.ini` in sync with `pyproject.toml` when changing dependency requirements.

## Releasing

Versions come from git tags (via `setuptools-scm`). Pushing a tag like `v1.2.3` runs the tests, builds, and publishes to PyPI:

```bash
git tag v1.2.3 && git push origin v1.2.3
```

Publishing uses PyPI trusted publishing: add this repository as a trusted publisher on PyPI (workflow `release.yml`, environment `pypi`).

## License

MIT -- see [LICENSE](LICENSE).
