# Reports

Moneybird can generate a variety of financial reports. These are read-only -- the CLI fetches the report data from the API.

## Fetching a report

```bash
moneybird reports get <TYPE> [--period PERIOD] [--granularity month|quarter|year] [...]
```

Not every option applies to every report: `--granularity` splits most period reports into months/quarters/years, `--period-until` is used by the aging reports, `--project-id` by `profit_loss` and `journal_entries`, `--financial-account-id` by `cash_flow`, and `--contact-id`, `--ledger-account-id`, `--account-type` by `journal_entries`. Paginated reports accept `--page` and `--per-page`.

**Period formats:** `this_month`, `prev_month`, `this_quarter`, `prev_quarter`, `this_year`, `prev_year`, or a custom range like `202401..202412`.

## Available report types

### Profit & Loss

Shows revenue, expenses, and net profit over a period.

```bash
moneybird reports get profit_loss --period this_year
moneybird reports get profit_loss --period 202401..202406
```

### Balance sheet

A snapshot of assets, equity, and liabilities.

```bash
moneybird reports get balance_sheet
```

### Cash flow

Overview of money coming in and going out, broken down by ledger account.

```bash
moneybird reports get cash_flow --period this_quarter
```

### Bank balance and working capital

```bash
moneybird reports get bank_balance --period this_year --granularity month
moneybird reports get working_capital --period this_year
```

### Tax

Tax amounts grouped by tax rate -- useful for VAT returns.

```bash
moneybird reports get tax --period prev_quarter
```

### Debtors and creditors

Who owes you money, and who you owe money to.

```bash
moneybird reports get debtors
moneybird reports get debtors_aging --period-until this_month   # with aging buckets
moneybird reports get creditors
moneybird reports get creditors_aging
```

### Revenue and expenses by contact or project

```bash
moneybird reports get revenue_by_contact --period this_year
moneybird reports get expenses_by_project --period this_year
```

### Other reports

```bash
moneybird reports get general_ledger --period this_month
moneybird reports get journal_entries --period this_month
moneybird reports get subscriptions
moneybird reports get assets

```

## Exports

Auditfile (XAF), brugstaat and ledger account exports are generated in the background. Start one, then fetch it from downloads:

```bash
moneybird reports export auditfile --year 2024 --version 4.0
moneybird downloads list --type auditfile
moneybird downloads get <DOWNLOAD_ID> --output auditfile-2024.xaf
```
