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
```

### Downloading a PDF

```bash
moneybird sales-invoices pdf 123456789
moneybird sales-invoices pdf 123456789 --output invoice-acme.pdf
```

### Credit invoices

Create a credit note (negative invoice) from an existing invoice:

```bash
moneybird sales-invoices credit 123456789
```

## Estimates

Estimates (quotes/proposals) can be sent to customers before creating an invoice. When accepted, they can be converted into invoices in the Moneybird web interface.

```bash
moneybird estimates list --all --state open
moneybird estimates get 123456789
moneybird estimates create --contact-id 123 --estimate-date 2024-03-01
moneybird estimates send 123456789
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
```
