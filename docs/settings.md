# Settings & Configuration

These commands deal with reference data and integrations that you typically set up once.

## Ledger accounts

Ledger accounts (grootboekrekeningen) are the categories in your chart of accounts. Every financial transaction is booked to one. Moneybird comes with a default set, but you can customize them.

```bash
moneybird ledger-accounts list --all
moneybird ledger-accounts get 123456789

moneybird ledger-accounts create --name "Software Licenses" --account-type expenses
moneybird ledger-accounts update 123456789 --name "SaaS Subscriptions"
moneybird ledger-accounts delete 123456789
```

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
