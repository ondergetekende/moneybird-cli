# Reports

Moneybird can generate a variety of financial reports. These are read-only -- the CLI fetches the report data from the API.

## Fetching a report

```bash
moneybird reports get <TYPE> [--period PERIOD] [--contact-id ID] [--project-id ID]
```

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

### Tax

Tax amounts grouped by tax rate -- useful for VAT returns.

```bash
moneybird reports get tax --period prev_quarter
```

### Debtors and creditors

Who owes you money, and who you owe money to.

```bash
moneybird reports get debtors
moneybird reports get debtors_aging   # with aging buckets (30/60/90 days)
moneybird reports get creditors
```

### Revenue and expenses by contact or project

```bash
moneybird reports get revenue_by_contact --period this_year
moneybird reports get expenses_by_project --project-id 123
```

### Other reports

```bash
moneybird reports get general_ledger --period this_month
moneybird reports get journal_entries --period this_month
moneybird reports get subscriptions
moneybird reports get assets
```
