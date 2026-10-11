`extract_invoice` now returns everything it could read plus a list of what it couldn't, instead of raising on the first bad field. All 17 tests pass.

**What changed (`seam.py`)**
- **Partial results:** a missing or unreadable field comes back as `None`, and everything else is still returned.
- **Problems list:** the result has a new `problems` list with one entry per bad field, for example `{"field": "issue_date", "reason": "not a date", "value": "0Z/10/2026"}`. For a missing field there is no `value`.
- **Incomplete marker:** `status` is `"incomplete"` whenever `problems` is non-empty. It wins over `mismatch`, and only `"ok"` is safe to post.
- **Line-level problems:**
  - A bad line is reported as `line 3 quantity` or `line 3 unit_price`, and the other lines are kept.
  - That line's `amount` is `None`.
  - `lines_total` is `None` unless every line has an amount, so a partial sum can't be mistaken for the real one.
- **Still an error:** `InvoiceError` is raised only when nothing usable comes out: empty text, an answer that isn't a JSON object, or no field readable at all.

**Compatibility**
- Code that only checks `status == "ok"` is safe.
- Code that assumed `issue_date`, `total` and similar fields are always set will now see `None` on incomplete invoices, so check the callers.
- The old single-field error tests (missing supplier, bad date, bad currency and so on) became incomplete-result tests, since those cases no longer raise.

I also added tests for your two examples (no invoice number, `0Z/10/2026`), a bad line, and the nothing-usable case, and rewrote the README section on `status` and errors.

**One behaviour to confirm:** an unreadable `description` is not treated as a problem, as before, because it doesn't affect the ledger amounts. Say if you want it flagged too.