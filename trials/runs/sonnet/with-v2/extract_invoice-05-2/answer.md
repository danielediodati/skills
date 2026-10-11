Invoices whose own figures are consistent, VAT included, now go straight to the ledger. The Brightwell invoice (309.00 + 61.80 VAT = 370.80) comes out `ok`. All 17 tests pass.

**What was wrong:** the tool compared the sum of the lines (309.00) to the amount due (370.80), so any invoice with VAT looked like a mismatch.

**What changed:**
- **`seam.py`:**
  - The model now reads the VAT amount as its own field. It reports 0 if the invoice shows none.
  - Code checks that lines + VAT equal the total, to the cent with no tolerance.
  - The result now includes `vat`, and `lines_total` is the net.
- **`test.py`:** the Brightwell case is now the baseline. I added tests for an invoice without VAT, VAT that doesn't add up (mismatch), and a missing `vat` field.
- **`README.md`:** updated to describe the new field and check.

**What still goes to the clerk:**
- An invoice where the lines, VAT and total don't add up, such as a wrong quantity or a mistyped total.
- An invoice where the model returns no VAT figure. This raises `InvoiceError` rather than guessing 0, so a missing figure can't slip through as consistent.

This matches `evals/extract_invoice/charter.md`, which already listed the net/VAT/total check as a code constraint not yet implemented. I didn't touch the charter.

One thing to watch: if an invoice states VAT only as a rate, with no amount, the model has to compute it or the invoice goes to review. Say if you see that layout often.