The extractor no longer guesses the issue date. All 20 tests pass, including new ones for the Brightwell and US cases.

**Why it went wrong.** The model was asked for `YYYY-MM-DD` directly, so it chose a day/month order silently. Nothing downstream could tell that "05/08/2026" had two readings.

**What changed in `seam.py`:**
- **Printed date:** the model now also returns `issue_date_as_printed`, the date exactly as it appears on the invoice. The code checks that string really occurs in the invoice text and parses it itself. The model's own ISO date is ignored.
- **Unambiguous dates** are read normally: `25/08/2026`, `2 Oct 2026`, `2026-08-25`, `05/05/2026`, and dotted dates (`dd.mm.yyyy`, treated as day-first by convention).
- **Ambiguous numeric dates** (`05/08/2026`, `03/04/2026`) with no order given come back with:
  - `issue_date = None`
  - `issue_date_candidates = [8 May, 5 Aug]`
  - `status = "date_ambiguous"`, which goes to a clerk, the same as `mismatch`.
- **Date order per supplier:** `extract_invoice(text, model, date_order="DMY")` (or `"MDY"`) resolves them. With `DMY`, Brightwell loads as 5 August 2026. The US supplier with `MDY` loads as 4 March.
- If both the totals and the date are in doubt, `status` stays `mismatch`, and `issue_date` is still `None`.

**What you need to do:**
- **Date order:** without a `date_order` for the supplier, Brightwell's invoice will be held for review rather than loaded. You need to keep a supplier-to-order mapping (Brightwell → `DMY`) and pass it in. I deliberately didn't infer it from currency or the model's guess, because that is how the original error got in.
- **Status handling:** any code that treats only `"ok"` as ledger-ready is fine. Anything that reads `issue_date` directly must now handle `None`.
- **Stray file:** while working I accidentally wrote a copy of `seam.py` into the parent directory (`...\sonnet\without\seam.py`). I couldn't move or delete it because that was blocked, so please delete it. The correct file is in `extract_invoice-07-3`.

I didn't update the README for the new field and status; say if you want that.