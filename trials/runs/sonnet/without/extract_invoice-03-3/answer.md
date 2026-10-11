An invoice with unreadable parts now comes back with everything that could be read, plus a list of what to fix. I could not run the tests: the shell was denied for the rest of the session, so please run `python -m unittest` in that directory.

**Behaviour (`seam.py`)**
- **Unreadable field:** the field comes back as `None` and is listed in `problems`. This covers supplier, invoice number, date, currency and total.
- **Unreadable line:** only that line's `quantity`, `unit_price` and `amount` become `None`, and the other lines stay intact. A missing quantity on line 3 is reported as `line 3 quantity`.
- **Problem entries:** each is `{"field": ..., "problem": ...}`. For your two examples, the first reports `invoice_number is missing` and the second reports `issue_date is not a date: '0Z/10/2026'`, so the clerk sees the garbled value.
- **Marking:** such an invoice gets `status: "incomplete"`, alongside the existing `ok` and `mismatch`. `incomplete` takes precedence over `mismatch`.
- **Sums:** `lines_total` is `None` when any line has no amount, so a partial sum can't pass as a real figure.
- **Errors:** `InvoiceError` is still raised for empty text, an answer that isn't a JSON object, or an answer where nothing at all is readable.

**Other changes**
- `README.md` documents the new `problems` field, the three statuses, and the rule that only `ok` goes to the ledger.
- In `test.py`, the old "missing X is an error" tests now assert the incomplete result. I also added tests for the invoice-number and `0Z/10/2026` cases, a partly unreadable line, and the nothing-usable error.

**Check callers:** `status` has a new value and the result has a new key. Any code that decides ledger eligibility by `status != "mismatch"` would now let `incomplete` through, so it should check `status == "ok"`. Code that assumed `issue_date`, `total` and similar are never `None` also needs a look.