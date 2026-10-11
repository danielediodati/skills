Invoices whose own figures are consistent now go through as `ok`, including ones with VAT, so Brightwell BP-2291 no longer lands in the review pile. All 18 tests pass.

**What was wrong:** the tool asked for only the lines and the amount due, then compared lines (309.00) to the total (370.80). Any invoice with VAT therefore failed.

**What changed** (in `seam.py`):
- The model is now also asked for the `subtotal` (if the invoice shows one) and the `tax`, the total VAT charged.
- An invoice is `ok` when lines + tax = total due. If the invoice states a subtotal, the lines must also match that.
- A missing tax counts as 0, so invoices without VAT behave as before.
- The result gains `subtotal` and `tax` fields. `README.md` and `test.py` are updated to match.

**Still flagged as `mismatch`:**
- A wrong quantity or price, because the lines no longer match the subtotal or the total.
- A mistyped total.
- VAT shown on the invoice but not included in the amount due.

**Limits:**
- The tool does not check that the VAT is the right percentage of the lines. It only checks that the invoice's own figures add up. If you also want to catch a wrong VAT rate, that is a separate check.
- If the model fails to read the VAT line from an invoice, that invoice will still go to a clerk. It will not slip through unchecked.

I tested with the fake model the test suite uses, not a real model on real invoice text. It is worth running a batch of real invoices to confirm the model reliably picks up the VAT figure.