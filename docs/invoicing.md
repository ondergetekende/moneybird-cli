# Invoicing

Moneybird's core function is invoicing. The CLI supports the full invoicing workflow: creating drafts, sending invoices, tracking payments, downloading PDFs, and issuing credit notes.

## Sales invoices

Sales invoices are invoices you send to your customers.

### Listing invoices

```bash
# First page
moneybird sales-invoices list

# Filter by state and period
moneybird sales-invoices list --state open --period this_month
moneybird sales-invoices list --state paid --period prev_year
moneybird sales-invoices list --contact-id 123456789

# All invoices
moneybird sales-invoices list --all
```

**States:** `draft`, `open`, `scheduled`, `pending_payment`, `reminded`, `late`, `paid`, `uncollectible`.

**Period formats:** `this_month`, `prev_month`, `this_quarter`, `prev_quarter`, `this_year`, `prev_year`, or a custom range like `202401..202406`.

### Finding a specific invoice

```bash
# By internal ID
moneybird sales-invoices get 123456789

# By invoice number (e.g., "2024-0042")
moneybird sales-invoices find 2024-0042
```

### Creating an invoice

Invoices are created as drafts. You need at least a contact ID:

```bash
moneybird sales-invoices create --contact-id 123456789
```

Optional fields: `--invoice-date`, `--first-due-interval` (days until due), `--reference`, `--currency`, `--discount`, `--workflow-id`, `--document-style-id`.

### Sending an invoice

Sending transitions the invoice from draft to open and delivers it to the customer:

```bash
moneybird sales-invoices send 123456789
moneybird sales-invoices send 123456789 --delivery-method Peppol
moneybird sales-invoices send 123456789 --email-address override@example.com
```

### Registering payments

When a customer pays:

```bash
moneybird sales-invoices pay 123456789 --amount 121.00 --date 2024-03-15
moneybird sales-invoices pay 123456789 --amount 121.00 --date 2024-03-15 --financial-mutation-id 456
moneybird sales-invoices delete-payment 123456789 <PAYMENT_ID>
moneybird sales-invoices pay-credit 123456789   # settle a credit invoice
```

### Reminders and collection

```bash
moneybird sales-invoices send-reminder --contact-id 123 --invoice-id 456 --invoice-id 789 \
  --workflow-id 1 --document-style-id 2 --identity-id 3
moneybird sales-invoices pause 123456789    # pause the payment workflow
moneybird sales-invoices resume 123456789
moneybird sales-invoices mark-dubious 123456789 --date 2024-06-01
moneybird sales-invoices mark-uncollectible 123456789 --date 2024-12-31
```

### Downloading a PDF

```bash
moneybird sales-invoices pdf 123456789
moneybird sales-invoices pdf 123456789 --output invoice-acme.pdf
moneybird sales-invoices pdf 123456789 --packing-slip
moneybird sales-invoices ubl 123456789          # UBL/XML e-invoice
moneybird sales-invoices find-by-reference "PO-1234"
```

### Notes and attachments

Sales invoices, estimates, external/recurring invoices, documents, contacts and time entries support notes; invoices, estimates and documents support attachments:

```bash
moneybird sales-invoices note 123456789 "Called customer" --todo
moneybird sales-invoices delete-note 123456789 <NOTE_ID>
moneybird sales-invoices attach 123456789 contract.pdf
moneybird sales-invoices download-attachment 123456789 <ATTACHMENT_ID> --output contract.pdf
moneybird sales-invoices delete-attachment 123456789 <ATTACHMENT_ID>
```

### Credit invoices

Create a credit note (negative invoice) from an existing invoice:

```bash
moneybird sales-invoices credit 123456789
```

## Estimates

Estimates (quotes/proposals) can be sent to customers before creating an invoice.

```bash
moneybird estimates list --all --state open
moneybird estimates get 123456789
moneybird estimates create --contact-id 123 --estimate-date 2024-03-01
moneybird estimates send 123456789
moneybird estimates find 2024-0001          # by estimate number
moneybird estimates pdf 123456789
moneybird estimates change-state 123456789 accepted
moneybird estimates bill 123456789          # convert into a sales invoice
moneybird estimates delete 123456789
```

Filter options: `--state` (`draft`, `open`, `late`, `accepted`, `rejected`, `billed`, `archived`), `--period`, `--contact-id`.

## Recurring sales invoices

Recurring invoices are templates that Moneybird uses to automatically generate invoices on a schedule (e.g., monthly hosting fees).

```bash
moneybird recurring-sales-invoices list
moneybird recurring-sales-invoices get 123456789

# Create a monthly recurring invoice
moneybird recurring-sales-invoices create \
  --contact-id 123 \
  --frequency-type month \
  --frequency 1 \
  --invoice-date 2024-01-01

moneybird recurring-sales-invoices update 123456789 --frequency 3
moneybird recurring-sales-invoices delete 123456789
```

**Frequency types:** `day`, `week`, `month`, `quarter`, `year`.

## External sales invoices

External sales invoices represent invoices created outside of Moneybird (e.g., from another system) that you want to track in your books for accounting purposes.

```bash
moneybird external-sales-invoices list --state open --period this_year
moneybird external-sales-invoices get 123456789
moneybird external-sales-invoices create --contact-id 123 --reference "EXT-001"
moneybird external-sales-invoices update 123456789 --reference "EXT-001-v2"
moneybird external-sales-invoices delete 123456789

# Create one from a PDF and let Moneybird read it
moneybird external-sales-invoices create-from-file invoice.pdf

# Payments and collection
moneybird external-sales-invoices pay 123456789 --amount 121.00 --date 2024-03-15
moneybird external-sales-invoices mark-uncollectible 123456789
```
