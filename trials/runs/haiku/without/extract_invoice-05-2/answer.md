Invoices whose figures are internally consistent now pass to the ledger, including VAT invoices like Brightwell BP-2291. The review pile now holds only invoices where the lines plus VAT don't equal the amount due. All 16 unit tests pass.

**The cause:** `status` compared the net sum of the lines (309.00) with the amount due, which includes VAT (370.80). The extraction prompt never asked for the VAT amount, so there was nothing to add back. Every VAT invoice was flagged.

**The fix** (`seam.py`):
- The prompt now asks the model for a `vat` field: the total VAT amount, or 0 if none is shown.
- `status` is `ok` when `lines_total + vat == total`, and `mismatch` otherwise.
- The result dict includes `vat`.

**Tests and docs:**
- The sample answer in `test.py` is now the Brightwell invoice (VAT 61.80, total 370.80), and it comes out `ok`.
- New cases: a no-VAT invoice that matches passes, a wrong total is flagged, and a wrong VAT amount is flagged.
- The rounding test sets `vat=0` explicitly.
- `README.md` describes the new rule.

**Things to know:**
- The tests use a fake model, so I haven't checked the new prompt against a live model. Run a few real invoices through it before relying on it.
- If the model reads the VAT wrongly or leaves it out, the invoice goes to review. That fails safe, but a model that often misreads VAT would refill the pile, so watch the first batch.
- The check is only "lines + VAT = amount due". It doesn't check quantity × unit price against the printed line amounts, which the model doesn't extract. A wrong quantity still gets caught only when it throws the total off.
- The directory isn't a git repo, so I haven't committed anything.