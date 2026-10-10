VAT invoices are now checked as lines plus tax, so your stationery example comes back `ok`. All 18 tests pass, including four new ones for tax.

- **Extraction:** the prompt in `seam.py` now asks the model for a `tax` amount and says line prices are net and `total` is the amount due, tax included.
- **Result:** the dict has a new `tax` key (a `Decimal`, rounded to cents) next to `lines_total` and `total`.
- **Status:** `ok` when `lines_total + tax == total`, otherwise `mismatch`.
- **No tax:** if the model returns no `tax` or `null`, it is `0.00` and the check behaves as before. A tax value that isn't a number raises `InvoiceError` ("tax is not a number").
- **Docs and tests:** `README.md` describes the new field and rule, and `test.py` covers the new cases.

The tests use a fake model, so the real extraction of tax from invoice text depends on your model following the updated prompt. It's worth running a few real VAT invoices through it.