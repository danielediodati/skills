A partly unreadable invoice now comes back with everything that could be read, plus a list of the fields that couldn't be. The 17 tests pass.

**Behaviour**
- **Bad fields:** A missing or unreadable field is returned as `None` and named in a new `missing` list. Line problems are named by line, e.g. `lines[2].quantity`.
- **Status:** Any invoice with a non-empty `missing` list gets status `incomplete`, so it can't be mistaken for `ok`. `incomplete` takes precedence over `mismatch`.
- **Your examples:** The no-invoice-number invoice returns supplier, date, currency, six lines and total, with `missing == ["invoice_number"]`. The `0Z/10/2026` scan returns everything else, with `missing == ["issue_date"]`.
- **Totals:** `lines_total` is only computed when every line amount is known; otherwise it's `None`.
- **Errors:** `InvoiceError` is raised only when the answer isn't a JSON object, or when not a single field is readable (e.g. `{}`). Empty text is still refused before the model is called.

**Charter**
The extract_invoice charter listed "anything else raises `InvoiceError`" as a constraint, so this change moves that line. I updated the charter's output and constraint wording to match; there's no git here, so there's no commit to keep them together.

**Prompt**
I added one sentence telling the model to use `null` for a field that is absent or unreadable. The model's reading decisions are unchanged.

**Decision for you**
The charter's ledger rule used to be implicit in the error. Now the only thing keeping an incomplete invoice out of the ledger is the caller checking `status == "ok"`. If you have downstream code that loads anything without an error, it should check `status`.

The changes are in `seam.py`, `test.py`, `README.md` and `evals/extract_invoice/charter.md`.