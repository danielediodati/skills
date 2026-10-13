The ledger no longer gets a guessed date. A numeric date that could be read two ways is now flagged for a clerk instead of loaded. All 19 tests pass, including new ones for the two cases you described.

**Cause:** the prompt asked the model for `YYYY-MM-DD`, so the model silently decided what "05/08/2026" meant, and the code accepted any valid ISO date. Nothing recorded that a guess had been made.

**What changed** (`seam.py`):
- **Date as printed:** the model now returns `issue_date_text`, copied exactly as printed, and the code parses it. If that text doesn't appear in the invoice, it raises `InvoiceError`.
- **Unambiguous dates:** these load as `ok`. That covers a month name ("5 Aug 2026"), an ISO date, a dotted date ("05.08.2026"), and a slashed date where one part is above 12 ("25/08/2026").
- **Ambiguous dates:** a slashed or dashed date like "05/08/2026" or "03/04/2026" with no supplier hint comes back with `issue_date=None`, `issue_date_candidates=[5 Aug, 8 May]`, and `status="ambiguous_date"`. A loader that reads `issue_date` fails loudly rather than loading a wrong date.
- **Supplier hint:** `extract_invoice(text, model, date_order="DMY")` resolves numeric dates deterministically. Brightwell's "05/08/2026" becomes 5 August 2026 and loads as `ok`; "MDY" gives 4 March for your US supplier.

**What you need to do:**
- Store a date order per supplier (Brightwell `"DMY"`, US suppliers `"MDY"`) and pass it in. Until you do, every slashed date that can be read two ways goes to a clerk.
- Treat any status other than `ok` as "not for the ledger". `ambiguous_date` is a new value alongside `mismatch`, so check that your loader doesn't only test for `mismatch`.
- If an invoice has both a bad total and an ambiguous date, `status` shows only `mismatch`. The ambiguity still shows in `issue_date=None` and `issue_date_candidates`, and it will surface once the total is fixed.

**Not changed:**
- A supplier who prints dates in a different order than their usual convention will still be read per the hint. The hint is only as good as the supplier master.
- I made the edits with the edit tool because my first scripted attempt was blocked. The README documents the new argument and status.