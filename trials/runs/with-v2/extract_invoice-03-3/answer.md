I made the part that fits inside the extractor's charter, but not the returned "incomplete" record you asked for. The tests pass (16).

**What changed (`seam.py`, `test.py`)**
- `extract_invoice` now reads every field before failing and reports all the problems at once, instead of stopping at the first.
- `InvoiceError` carries three new attributes:
  - `missing`: the missing or unreadable fields, such as `["invoice_number", "issue_date"]` or `["line 2 quantity"]`.
  - `partial`: everything that was read, with `None` where a value couldn't be read. Line amounts are still computed by code.
  - `unreadable`: the raw text of values that were present but bad, such as `{"issue_date": "0Z/10/2026"}`.
- It is still an error, so an incomplete invoice can't reach the ledger. The clerk's form can be pre-filled from `error.partial` and ask only for the fields in `error.missing`.
- If the model's answer isn't JSON at all, or the text is empty, there is no partial data, as before.

**What I did not do, and why**
The charter (`evals/extract_invoice/charter.md`) lists the answer's shape as constrained: anything missing or malformed raises `InvoiceError`, and the only statuses are `ok` and `mismatch`. Returning a record with an `incomplete` status would move that line, and only you can change the charter.

**The decision for you**
If you want the function to return the incomplete record itself, with a status like `incomplete` and a `missing` list, the charter's "Constrained" entry on the answer's shape and its output description need to change first. That would let callers handle one return value instead of catching an exception. The cost is that anything that only checks `status == "ok"` must now also cope with a third status. If you update the charter, I'll make the change.