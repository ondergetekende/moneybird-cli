# Time Tracking

Moneybird includes built-in time tracking, letting you log hours against projects and contacts. Tracked time can be invoiced directly.

## Projects

Projects group time entries and financial records together. They're useful for tracking profitability per client engagement or internal initiative.

```bash
moneybird projects list
moneybird projects list --state active
moneybird projects list --state archived

moneybird projects get 123456789

moneybird projects create --name "Website Redesign" --budget 5000
moneybird projects update 123456789 --budget 7500
moneybird projects delete 123456789
```

## Time entries

Time entries record the actual hours worked. Each entry has a start and end time, and can optionally be linked to a contact and project.

### Listing time entries

```bash
moneybird time-entries list
moneybird time-entries list --all --period this_month
moneybird time-entries list --project-id 123
moneybird time-entries list --contact-id 456
moneybird time-entries list --user-id 789
moneybird time-entries list --state open
```

**States:** `all`, `open` (not yet invoiced), `non_billable`.

### Managing time entries

```bash
moneybird time-entries get 123456789

# Log 2 hours of work
moneybird time-entries create \
  --started-at "2024-03-15T09:00:00" \
  --ended-at "2024-03-15T11:00:00" \
  --description "Frontend development" \
  --project-id 123 \
  --contact-id 456 \
  --billable

moneybird time-entries update 123456789 --description "Frontend + API work"
moneybird time-entries delete 123456789
```
