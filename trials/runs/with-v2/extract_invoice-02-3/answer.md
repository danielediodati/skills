VAT is now reported as its own amount, and an invoice is `ok` when the lines plus VAT equal the total. All 18 tests pass, including four new ones. I did not run it against a real model, so the prompt change is untested end to end.

**`seam.py`**
- The prompt now asks the model for `vat`, the tax amount as shown on the invoice (0 if there is none), and says line prices are net.
- The result has a new `vat` field next to `lines_total` and `total`.
- `status` is `ok` only if `lines_total + vat == total`, to the cent with no tolerance, so a wrong record still goes to a clerk.
- If `vat` is missing or null it counts as `0.00`, so invoices without tax behave as before. A non-numeric `vat` raises `InvoiceError("vat is not a number…")`.

**`test.py`**: your stationery example (309.00 + 67.98 = 376.98) comes out `ok`. VAT that doesn't add up is `mismatch`. A no-VAT invoice gives zero VAT. An unreadable VAT is an error.

**`README.md`** describes the new field and status rule.

This matches the "Net, VAT and total as separate fields" line already in the `extract_invoice` charter, which marked it as not yet in code. I did not touch the charter.

One thing to watch: if the model drops the VAT on an invoice that has it, that invoice comes back `mismatch` rather than `ok`. That is the safe direction, but it means the model's reading of the VAT line is what decides these invoices.