# Documents

Moneybird organizes expenses and other bookkeeping records as "documents." There are several types, each serving a different purpose. They all share the same basic command structure.

## Document types

- **Purchase invoices** -- invoices you receive from suppliers. These are your expenses.
- **Receipts** -- proof-of-payment records for expenses (e.g., a store receipt).
- **General documents** -- catch-all for financial records that don't fit other categories.
- **Journal documents** -- manual bookkeeping entries for corrections and adjustments.
- **Typeless documents** -- uploaded files whose type hasn't been determined yet (e.g., documents uploaded via email or the bulk uploader).

## Common commands

All document types support the same operations. Replace `<type>` with one of: `purchase-invoices`, `receipts`, `general-documents`, `journal-documents`, `typeless-documents`.

### Listing

```bash
moneybird <type> list
moneybird <type> list --all --period this_month
```

### Viewing

```bash
moneybird <type> get 123456789
```

### Creating

```bash
# Purchase invoice from a supplier
moneybird purchase-invoices create --contact-id 123 --reference "INV-2024-001"

# Receipt
moneybird receipts create --contact-id 123 --reference "Albert Heijn" --date 2024-03-15

# General document
moneybird general-documents create --contact-id 123 --reference "Insurance Q1"

# Journal entry
moneybird journal-documents create --reference "Year-end correction" --date 2024-12-31
```

### Updating and deleting

```bash
moneybird <type> update 123456789 --reference "Updated reference"
moneybird <type> delete 123456789
```

## Assets

Assets represent significant purchases that are used over multiple years -- company cars, laptops, furniture, etc. Moneybird tracks their value and handles depreciation.

```bash
moneybird assets list
moneybird assets list --include-inactive
moneybird assets list --ledger-account-id 123
moneybird assets get 123456789
moneybird assets create --name "MacBook Pro" --purchase-date 2024-01-15 --purchase-value 2499
moneybird assets update 123456789 --name "MacBook Pro 16-inch"
moneybird assets delete 123456789
```
