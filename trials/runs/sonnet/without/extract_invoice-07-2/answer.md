Invoices are now loaded with the date as printed on them, and a day/month that could be swapped is flagged instead of guessed. All 18 tests pass, including new ones for the Brightwell and American cases.

**What was wrong:** in `seam.py` the model was asked for the date already converted to `YYYY-MM-DD`. For `05/08/2026` it had to guess the order, and the result was loaded with no sign of doubt.

**What changed in `seam.py`:**
- **Printed text:** the model now copies the date exactly as printed (`issue_date_text`) and no longer reformats it. The code works out the date from that text.
- **Clear dates:** a date is accepted as certain only when it can't be read two ways. That covers a day above 12 (`13/08/2026`), the same day and month (`05/05/2026`), a year-first date, or a written month (`5th August 2026`).
- **Swappable dates:** `05/08/2026` and `03/04/2026` get `issue_date = None`, `date_candidates = [5 Aug, 8 May]` and `status = "date_ambiguous"`. Nothing goes into the ledger as certain.
- **Known supplier convention:** `extract_invoice(text, model, date_order="DMY")` (or `"MDY"`) settles these automatically. Brightwell would be `DMY` and the American supplier `MDY`.
- **Both problems:** an invoice whose total doesn't match the lines still gets `status = "mismatch"`, and its date stays unset if it is ambiguous.

**Decisions for you:**
- **Per-supplier date order:** I didn't infer day-first or month-first from currency or country, because that is itself a guess. Whoever calls this needs a per-supplier setting for `date_order`; without it, every swappable date goes to a clerk.
- **Loader handling of `None`:** the ledger loader must treat `status == "date_ambiguous"` (and `issue_date is None`) as "send to a clerk". I haven't seen that code.

**Other changes:**
- **Tests:** the existing tests now use `issue_date_text`, and I changed the unreadable-date test input to "sometime in October".
- **README:** it now describes the new fields and the `date_order` option.