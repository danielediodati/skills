Partly unreadable invoices now come back with everything that could be read, plus a list of what couldn't. All 16 tests pass.

**Behaviour (`seam.py`)**
- Each unreadable field is `None` and listed in a new `problems` entry, for example `{"field": "issue_date", "reason": "issue_date is not a date: '0Z/10/2026'"}`.
- Line problems name the line, for example `lines[2].quantity`. The other lines, and the rest of that line, are kept.
- Any problem gives `status: "incomplete"`, so it can't be mistaken for `ok` or `mismatch`. Anything that only loads `ok` invoices into the ledger stays safe.
- `lines_total` is `None` when any line amount is unknown. `total` is `None` if it was unreadable.
- `InvoiceError` is still raised for empty text, an answer that isn't a JSON object, or an answer where nothing at all was usable.
- Your two examples now give: a result with `invoice_number: None` and all else intact, and a result with `issue_date: None` and all else intact.

**Tests and docs**
- The old "missing X is an error" tests became "incomplete" tests. I added one for an answer with nothing usable (`{}`), which still errors.
- The README describes the new contract.

**Decision for you**
- Any `ok`/`mismatch` consumer that reads fields like `issue_date` directly must now check `status` first, since those fields can be `None`.
- A line with a non-numeric description is not treated as a problem; only quantity and unit price are checked, as before.
- I kept `problems` as an always-present key (empty for `ok`/`mismatch`) so callers see one shape.