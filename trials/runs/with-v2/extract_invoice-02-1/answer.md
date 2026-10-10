VAT invoices now come back `ok` when the lines plus the tax equal the total, and the tax is reported as its own `tax` amount next to `lines_total` and `total`. All 18 tests pass.

- **Prompt:** it now asks the model for a `tax` field (the VAT amount, 0 if none) and says the lines are before tax and the total includes it. Reading the tax off the invoice stays with the model.
- **Check:** the arithmetic is done in code, as the charter's "Net, VAT and total" item requires. The status is `ok` only if `lines_total + tax == total` to the cent, with no tolerance.
- **No tax on the invoice:** a missing or null `tax` is treated as `0.00`, so those invoices behave exactly as before.
- **Unreadable tax:** a non-numeric `tax` raises `InvoiceError` ("tax is not a number").
- **Tests and README:** I added tests for your stationery example (309.00 + 67.98 = 376.98, `ok`), the no-tax case, mismatches with tax, and an unreadable tax. The README describes the new field.

I did not touch the charter. Its line saying the VAT split is "Not yet in code" is now out of date, and updating it is your call.