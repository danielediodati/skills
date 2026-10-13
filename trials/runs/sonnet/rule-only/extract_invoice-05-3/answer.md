Invoices that carry VAT are now checked as lines plus VAT against the amount due, so BP-2291 comes out as `ok` and goes to the ledger. All 16 tests pass, including two new ones for the VAT cases.

**Cause:** the check compared the sum of the lines (309.00) with the amount due (370.80). Any invoice with VAT therefore failed, even when every figure was right.

**Changes:**
- **`seam.py`:**
  - The prompt now also asks the model to report the VAT amount charged, with 0 if the invoice shows none.
  - The result has a new `vat` field.
  - Code decides the status: `ok` when `lines_total + vat == total`, otherwise `mismatch`.
- **`README.md` and `test.py`:** the README describes the new rule, and the new tests cover Brightwell (61.80 VAT, 370.80 due → `ok`) and a mistyped total with VAT (380.80 → `mismatch`).

**What still goes to review:**
- A wrong quantity or price, or a mistyped total, still lands in the review pile.
- An invoice with VAT where the model fails to report the VAT figure also goes to review, because the sum won't match.

**Not checked:** the code does not test that VAT is 20% (or any particular rate) of the lines. An invoice whose VAT figure is itself wrong, but whose total is consistent with that figure, will pass. If your clerks should catch that too, the rate would need to be checked as well, which is a policy decision for you.