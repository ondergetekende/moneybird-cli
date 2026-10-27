# Settings & Configuration

These commands deal with reference data and integrations that you typically set up once.

## Ledger accounts

Ledger accounts (grootboekrekeningen) are the categories in your chart of accounts. Every financial transaction is booked to one. Moneybird comes with a default set, but you can customize them.

```bash
moneybird ledger-accounts list
moneybird ledger-accounts get 123456789

moneybird ledger-accounts create --name "Software Licenses" --account-type expenses --rgs-code WMfoBelMfo
moneybird ledger-accounts update 123456789 --name "SaaS Subscriptions"
moneybird ledger-accounts delete 123456789
```

`--rgs-code` (an RGS 3.5 reference code) is required when creating a ledger account. Account types: `non_current_assets`, `current_assets`, `equity`, `provisions`, `non_current_liabilities`, `current_liabilities`, `revenue`, `direct_costs`, `expenses`, `other_income_expenses`.

## Tax rates

Tax rates define the VAT percentages available when creating invoices and expenses. These are pre-configured by Moneybird based on your country; the CLI provides read-only access so you can look up IDs.

```bash
moneybird tax-rates list
moneybird tax-rates list --all
```

The output includes the `id`, `name`, `percentage`, and whether the rate is `active`. Use the `id` when creating products or invoice lines that need a specific tax rate.

## Webhooks

Webhooks let you receive real-time HTTP notifications when things change in Moneybird -- for example, when an invoice is paid or a contact is created. This is useful for integrating Moneybird with other systems.

### Listing webhooks

```bash
moneybird webhooks list
```

### Creating a webhook

```bash
moneybird webhooks create \
  --url "https://example.com/webhooks/moneybird" \
  --events sales_invoice_state_changed \
  --events contact_created
```

You can specify `--events` multiple times to subscribe to several event types.

### Managing webhooks

```bash
moneybird webhooks activate 123456789
moneybird webhooks deactivate 123456789
moneybird webhooks delete 123456789
```

## Task lists

Task lists are checklists (e.g., for closing a month or year). They consist of groups, which contain tasks, and can be created from reusable templates.

```bash
moneybird task-lists list
moneybird task-lists create --name "Close Q1" --period-begin 2026-01-01 --period-end 2026-03-31
moneybird task-lists add-group 123 --name "Bank" --report-type balance_sheet
moneybird task-lists groups add-task 456 --name "Reconcile bank account"

moneybird task-lists tasks assign 789 <USER_ID>
moneybird task-lists tasks complete 789
moneybird task-lists tasks reopen 789
moneybird task-lists tasks note 789 "Waiting for statement"

# Templates
moneybird task-lists templates list
moneybird task-lists templates create --name "Quarterly close"
moneybird task-lists templates add-group 321 --name "VAT"
moneybird task-lists templates instantiate 321 --period-begin 2026-04-01 --period-end 2026-06-30
```

## Identities

Identities are the company details (name, address, bank account) shown on your invoices. Without an ID, `get` and `update` use the default identity.

```bash
moneybird identities list
moneybird identities get
moneybird identities update --tax-number NL001234567B01
moneybird identities create --company-name "Acme Labs" --address1 "Main St 1" --zipcode 1234AB \
  --city Amsterdam --country NL --email info@acme-labs.com
moneybird identities delete 123456789
```

## Lookups

IDs you need for other commands (workflows, document styles, users):

```bash
moneybird workflows list
moneybird workflows get 123456789
moneybird document-styles
moneybird custom-fields
moneybird users --include-inactive
moneybird verifications
```
