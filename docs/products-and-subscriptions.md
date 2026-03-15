# Products & Subscriptions

## Products

Products are reusable line items that you can add to invoices and estimates. Defining products saves time when you invoice the same thing repeatedly -- instead of typing the description, price, and tax rate each time, you reference a product.

### Listing products

```bash
moneybird products list
moneybird products list --query "hosting"
moneybird products list --currency USD
moneybird products list --all
```

### Finding a product

```bash
# By internal ID
moneybird products get 123456789

# By your own identifier/SKU
moneybird products find "HOSTING-PRO"
```

### Managing products

```bash
moneybird products create --title "Web Hosting Pro" --price 29.95 --tax-rate-id 123
moneybird products update 123456789 --price 34.95
moneybird products delete 123456789
```

Additional create/update fields: `--description`, `--currency` (default EUR), `--ledger-account-id`, `--identifier` (your SKU/product code).

## Subscriptions

Subscriptions represent ongoing service agreements with customers. Moneybird tracks the subscription lifecycle and can automatically generate invoices based on the subscription terms.

```bash
moneybird subscriptions list --all
moneybird subscriptions get 123456789

moneybird subscriptions create \
  --contact-id 123 \
  --product-id 456 \
  --frequency-type month \
  --frequency 1 \
  --start-date 2024-01-01

moneybird subscriptions update 123456789 --end-date 2025-01-01
moneybird subscriptions cancel 123456789
```

**Frequency types:** `day`, `week`, `month`, `quarter`, `year`.
