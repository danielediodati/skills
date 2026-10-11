VAT invoices now come back `ok` when the lines plus the tax equal the total, and the tax is reported as its own amount in the result. All 18 tests pass.

- **Tax field:** the result has a new `tax` key next to `lines_total` and `total`. The prompt now asks the model for the invoice's tax amount, with lines taken before tax and `total` as the amount due including tax.
- **Status:** `ok` when `lines_total + tax == total`, otherwise `mismatch`.
- **Invoices with no tax:** if the model returns no tax or `null`, `tax` is `0.00` and the check is the same as before.
- **Unreadable tax:** a non-numeric tax raises `InvoiceError` ("tax is not a number").
- **Changes:** the code is in `seam.py`, and I added tests to `test.py` for your stationery-supplier example, a total that doesn't match, no tax, and a bad tax value. The README describes the new field and the check.

The tax amount comes from the model, so a model that fails to extract the VAT line will report zero tax and the invoice will show as `mismatch` again.