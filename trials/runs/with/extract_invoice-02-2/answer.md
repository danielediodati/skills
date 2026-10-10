VAT invoices now come back `ok` when the lines plus the tax equal the total, and the tax is reported on its own. All 18 tests pass, including four new ones for tax. I didn't run it against a real model, so how well the prompt makes the model pick out the tax line is untested.

- **Prompt (`seam.py`):** the model now also returns `tax`, the VAT or other tax charged, and is told the lines are net and `total` is the amount due with tax included.
- **Result:** there is a new `tax` field (`Decimal`, in cents) next to `lines_total` and `total`.
- **Check:** `status` is `ok` only if `lines_total + tax == total`, to the cent. A missing or null `tax` counts as `0.00`, so invoices without tax behave exactly as before. A non-numeric `tax` raises `InvoiceError`.
- **Your example:** lines 309.00 + VAT 67.98 = 376.98, so it comes out `ok`.
- **Docs:** I updated `README.md` and `evals/extract_invoice/charter.md`. The charter already listed this arithmetic check as constrained but "not yet in code", so this change implements it rather than moving the line.

Because a missing `tax` is treated as 0, an invoice with VAT where the model leaves `tax` out will still come back `mismatch`. That is the safe direction, since a clerk checks it.