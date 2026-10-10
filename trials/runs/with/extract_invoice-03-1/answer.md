Partly unreadable invoices now come back with everything that could be read, plus a list of what couldn't, and a status of `incomplete`. All 16 tests pass.

**What it does now** (`seam.py`)
- **Unreadable fields:** any of supplier, invoice number, date, currency or total that is missing or unreadable comes back as `None`, and everything else is kept.
- **Problems list:** `problems` holds `{"field", "reason"}` entries, for example `issue_date` with `issue_date is not a date: '0Z/10/2026'`.
- **Lines:** a line with an unreadable quantity or unit price keeps its other values and gets `amount: None`. The problem is listed as `line 1 quantity`.
- **Lines total:** `lines_total` is `None` while any line is unreadable or there are no lines.
- **Status:** `incomplete` is set whenever `problems` is non-empty. Only `ok` is meant for the ledger, and code sets it, never the model.
- **Errors:** `InvoiceError` is still raised for empty text, an answer that isn't a JSON object, or when not a single field or line amount is usable.

**Charter and README changed in the same edit**
- This relaxes the charter's constraint "anything else raises `InvoiceError`", so I updated `evals/extract_invoice/charter.md` and the README to match.
- The model/code line is unchanged: the model still reads, and code decides completeness and status.
- The one-call budget is also unchanged.

**Decisions for you**
- **Return shape:** callers that only check `status == "ok"` are safe, but any caller that relied on exceptions for missing fields will now get a dict with `None` values and must check `status`.
- **Not-quite-empty answers:** "nothing usable" means no scalar field and no computable line amount. An answer with only a supplier name still comes back as `incomplete` rather than an error. Say if you'd rather set the bar higher.