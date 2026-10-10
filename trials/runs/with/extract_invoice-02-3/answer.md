VAT invoices now come back `ok` when the lines plus the tax equal the total. Your stationery example gives lines total 309.00, tax 67.98, total 376.98 and status `ok`. The 18 tests pass, including four new ones for tax.

- **Prompt:** the model is now asked for a `tax` amount (0 if none), and told that `total` is the amount due with tax included.
- **Result:** there is a new `tax` key next to `lines_total` and `total`.
- **Status:** `ok` only when `lines_total + tax == total` to the cent, otherwise `mismatch`.
- **No tax on the invoice:** a `tax` the model omits or returns as null counts as `0.00`, so those invoices behave as before. An unreadable `tax` raises `InvoiceError("tax is not a number")`.
- **Charter and README:** the charter's "Not yet in code" note on net/VAT/total is replaced with what the code now does, and the README describes the new field.

This is the line the charter already placed in code, so nothing moved. The model only reads the tax amount, and the arithmetic stays in code.

An invoice where the model reads the VAT as a line and also reports it as `tax` would count it twice and show `mismatch`, which is the safe direction. If you see that, the prompt needs to say tax is not a line.