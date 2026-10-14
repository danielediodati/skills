Invoices whose own figures add up now go straight to the ledger, and the Brightwell invoice (BP-2291) is one of them. All 19 tests pass.

**The cause:** the extractor compared the amount due, which includes VAT, against the sum of the lines, which doesn't. The prompt never asked for VAT or the subtotal, so every VAT invoice looked like a mismatch.

**The fix** (in `seam.py`, with the tests in `test.py` and the README updated to match):
- The model is now also asked for `subtotal` (before VAT) and `vat`. Either can be `null` if the invoice doesn't show it.
- `status` is `ok` when the lines give the subtotal, and the subtotal plus VAT gives the total. When no subtotal or VAT is shown, it checks the lines against the total as before.
- The result dict includes `subtotal` and `vat`.

**Tests added:**
- Brightwell BP-2291 (309.00 + 61.80 = 370.80) comes out `ok`.
- An amount due that doesn't match is `mismatch`.
- A VAT figure that doesn't match the subtotal is `mismatch`.
- Lines that don't match the stated subtotal are `mismatch`.
- `null` VAT and subtotal are accepted.

**Things to know:**
- The check trusts the VAT and subtotal the model reads. If the model misreads them in a way that makes a wrong total appear to add up, the invoice passes. A mistyped total on a VAT invoice will still be caught unless the VAT is misread in the same way.
- If the model returns `null` for VAT on an invoice that has VAT, the invoice still goes to the clerk. That is the safe direction, but it means some correct invoices will keep landing in the pile. Check the pile after a run on real invoices to see how often this happens.
- Invoices that show VAT-inclusive unit prices will go to the clerk, because the lines won't match the subtotal in that case.
- I haven't run this against the real invoice text or the real model, only the fake model in the tests. I'd suggest running a batch of recent invoices, both VAT and non-VAT, and checking the pile before relying on it.
- The folder is not a git repository, so I didn't commit anything.