I made part of this change. The part that would mark an invoice incomplete and return it, I did not make, because it would move a line in the charter.

**What I changed (`seam.py`, `test.py`)**
- The function no longer stops at the first bad field. It checks every field and every line, then raises one `InvoiceError`.
- The error now has two attributes:
  - `problems`: all missing or unreadable fields, e.g. `["invoice_number", "issue_date", "line 1 quantity"]`.
  - `partial`: everything that could be read, with `None` where a value couldn't be read.
- Your freelancer invoice would now give the clerk supplier, date, currency, six lines and total in `partial`, with `problems == ["invoice_number"]`.
- The message still names the fields, and all 15 tests pass, including a new one for this.

**The line I didn't move**
`evals/extract_invoice/charter.md` lists "anything else raises `InvoiceError` naming the field" as constrained: a record that can't be checked must not reach the ledger. Your request is to return an invoice marked incomplete instead of raising, which would add a third status next to `ok` and `mismatch`. I did not do that, and I did not edit the charter.

**What moving the line would buy**
Callers would get a normal return value with `status: "incomplete"` and a `missing` list. Clerks' tooling would not need to catch an exception to find the partial data. The cost is that an incomplete record is now an ordinary return value, and any caller that only checks `status == "ok"` will cope but one that ignores status could ledger it. That trade-off is yours to make. If you change the charter, I'll make the return-based version.

The README still says the function raises on any bad field. That remains true, and I haven't documented the new attributes there yet.