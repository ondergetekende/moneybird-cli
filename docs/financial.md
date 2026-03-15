# Financial

These commands deal with bank accounts, transactions, and the bookkeeping side of Moneybird.

## Financial accounts

Financial accounts represent your bank accounts, credit cards, and other payment methods. They are configured in Moneybird's web interface; the CLI can list them so you can look up their IDs for use in other commands.

```bash
moneybird financial-accounts list
```

## Financial mutations

Financial mutations are the individual transactions on your financial accounts -- the lines on your bank statement. Moneybird imports these automatically if you have a bank connection set up, or you can upload them manually via bank statements.

Each mutation can be "booked" (linked) to an invoice, expense, or ledger account to reconcile your books.

```bash
# List mutations
moneybird financial-mutations list --period this_month
moneybird financial-mutations list --state unprocessed
moneybird financial-mutations list --mutation-type credit
moneybird financial-mutations list --financial-account-id 123

# View details
moneybird financial-mutations get 123456789

# Link a mutation to a sales invoice
moneybird financial-mutations link 123456789 \
  --booking-type SalesInvoice \
  --booking-id 987654321

# Unlink
moneybird financial-mutations unlink 123456789 \
  --booking-type Payment \
  --booking-id 111222333
```

**States:** `all`, `unprocessed`, `processed`.
**Mutation types:** `all`, `debit`, `credit`.

## Financial statements

Financial statements group mutations together, typically representing a bank statement or import batch. You usually don't need to create these manually -- Moneybird creates them when you import bank data. But for custom integrations:

```bash
moneybird financial-statements create \
  --financial-account-id 123 \
  --reference "Statement March 2024" \
  --official-date 2024-03-31 \
  --official-balance 12345.67

moneybird financial-statements update 123456789 --official-balance 12400.00
moneybird financial-statements delete 123456789
```

## Payments

Payments are records of money received or paid, linked to invoices and other documents. They are usually created through the invoice commands (`sales-invoices pay`), but you can look up individual payments:

```bash
moneybird payments get 123456789
```

## Purchase transactions

Purchase transactions represent outgoing payments to suppliers. They are typically created through Moneybird's payment batches (SEPA transfers), but you can list and inspect them:

```bash
moneybird purchase-transactions list --state pending_payment
moneybird purchase-transactions list --period this_month
moneybird purchase-transactions get 123456789
moneybird purchase-transactions delete 123456789  # only pending ones
```

**States:** `all`, `open`, `pending_payment`, `paid`, `cancelled`.
