Invoices with VAT now come back `ok` when the lines plus the tax equal the total. The test suite passes (18 tests, including 4 new ones). I did not run it against a real model.

- **Prompt:** the model is now asked for a `tax` amount (0 if the invoice shows none) and told that lines are net and `total` includes tax.
- **Result:** there is a new `tax` field next to `lines_total` and `total`.
- **Status:** it is `ok` when `lines_total + tax == total`, otherwise `mismatch`.
- **No-tax invoices:** if the model omits `tax` or returns null, it is treated as `0.00`, so those invoices behave as before.
- **Bad tax values:** an unreadable `tax` raises `InvoiceError` ("tax is not a number").

Your stationery example (309.00 + 67.98 = 376.98) is covered by a new test and comes back `ok`. The README documents the new field.

The change relies on the model reporting the tax figure from the invoice. If it misses the VAT line and returns no tax, that invoice will still show as `mismatch`, which is the correct outcome for a clerk to review.

The changes are in `seam.py`, `test.py` and `README.md`.