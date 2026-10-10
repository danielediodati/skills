I did only part of what you asked, because the rest would move a line the charter sets.

**Done (all 16 tests pass, including two new ones):**
- `InvoiceError` now carries `missing` (the fields that are missing or unreadable, e.g. `invoice_number`, `issue_date`, `lines[2].quantity`) and `partial` (everything that could be read).
- The function reports every unreadable field in one pass instead of stopping at the first. The message names all of them.
- In `partial`, line amounts are still computed by code, and `lines_total` is included when every line is readable.
- `partial` has no `status`, so it cannot be mistaken for a ledger-ready record.
- The README documents this. It is still one model call, with no retry.

For your two examples, the missing invoice number gives `missing=["invoice_number"]` and `partial` holds the supplier, date, currency, six lines and the total. The `0Z/10/2026` date gives `missing=["issue_date"]` and `partial` holds the rest.

**Not done: returning an incomplete invoice as a normal result instead of raising.**
- **The line:** the charter's Constrained section says a wrong shape "raises `InvoiceError` naming the field", and `status` is only `ok` or `mismatch`. An `incomplete` result would replace that error with a returned record and add a status. Only you can change the charter, so I left it alone.
- **What moving it would buy:** callers could treat a partial invoice as a return value and branch on `status == "incomplete"` instead of catching an exception. Today they must catch `InvoiceError` and read `.partial` and `.missing`. The safety is the same, since neither path reaches the ledger unless the caller chooses.

If you want the returned-record version, tell me and update the charter, or authorise me to, and I'll make it.