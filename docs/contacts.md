# Contacts

Contacts in Moneybird represent the people and companies you do business with -- your customers, suppliers, and other relations. Every invoice, estimate, and subscription is tied to a contact.

## Listing contacts

```bash
# First page (default)
moneybird contacts list

# All contacts, including archived ones
moneybird contacts list --all --include-archived
```

## Searching and filtering

Search by name, email, phone number, or customer ID:

```bash
moneybird contacts search "Acme"
```

Filter by specific criteria:

```bash
moneybird contacts filter --created-after 2024-01-01
moneybird contacts filter --updated-after 2024-06-01
moneybird contacts filter --last-name "Vries"
```

## Viewing a contact

```bash
moneybird contacts get 123456789
```

## Creating a contact

A contact needs at least a company name, or a first and last name:

```bash
# Company
moneybird contacts create --company-name "Acme Corp" --email info@acme.com

# Individual
moneybird contacts create --firstname "Jan" --lastname "de Vries" --email jan@example.com
```

Additional fields: `--phone`, `--address1`, `--address2`, `--zipcode`, `--city`, `--country` (two-letter code like `NL`), `--delivery-method` (`Email`, `Peppol`, `Post`, `Manual`). `--email` sets the address invoices are sent to.

## Finding duplicates

```bash
moneybird contacts doubles
```

## Updating and deleting

```bash
moneybird contacts update 123456789 --email new@example.com
moneybird contacts delete 123456789
```

## Archiving

Archiving hides a contact from default lists without deleting it and its associated records:

```bash
moneybird contacts archive 123456789
```
