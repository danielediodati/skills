Invoices whose figures are consistent, VAT included, now come back as `ok`, so BP-2291 goes straight to the ledger. The unit tests pass (19, including new VAT cases). I couldn't check it against a real model's answers.

**Cause:** the tool only compared the sum of the lines (309.00, which is before VAT) with the amount due (370.80). Any invoice with VAT therefore looked like a mismatch.

**Change in `seam.py`:**
- The prompt now also asks the model for the invoice's `subtotal` (before VAT) and `vat` (total VAT amount), both null if the invoice doesn't show them.
- An invoice is `ok` when lines + VAT equals the total. If a subtotal is stated, it must also equal the lines.
- The result gains a `vat` field (zero when none is stated). Invoices without VAT behave exactly as before.

**Still flagged as `mismatch`:**
- a mistyped or wrong total;
- a wrong quantity or unit price, because the lines then no longer match the printed subtotal or total;
- a subtotal that doesn't match the lines.

**Tests and README:** I added tests for the Brightwell figures, a wrong total with VAT, a wrong quantity with VAT, and a subtotal that doesn't match the lines. The README now describes the VAT rule.

**Limitation:** the check relies on the model reading the printed VAT figure correctly. If it returns no VAT for an invoice that has VAT, that invoice goes to review as before. That is the safe direction, but it would show up as a few false mismatches, so it's worth watching on real invoices.