Your stationery invoice now comes back `ok`, with the VAT reported as its own amount. All 18 tests pass, including four new ones for VAT.

- **Result:** a new `vat` key sits next to `lines_total` and `total`. For your example that gives 309.00, 67.98 and 376.98.
- **Status:** `ok` when `lines_total + vat == total` to the cent, otherwise `mismatch`.
- **No tax:** when the invoice has no tax, or the model returns no `vat`, `vat` is `0.00`, so those invoices behave as before.
- **Unreadable VAT:** a `vat` the model returns that isn't a number raises `InvoiceError("vat is not a number…")`, like the other amounts.
- **Who does what:** the model only reads the VAT amount off the invoice (the prompt now asks for `vat`, and says `total` is the amount due including tax). The addition and the comparison stay in code.

This was already listed in `evals/extract_invoice/charter.md` as a constrained item "not yet in code", so I updated that note and the "lines must add up" line to match what the code now does. I also updated `README.md`.

One thing to be aware of: a VAT invoice whose model answer leaves out `vat` is treated as having no tax and will still come back `mismatch`.