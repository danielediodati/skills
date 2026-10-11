Invoices with VAT whose figures are consistent now come out `ok` and go straight to the ledger. All 18 tests pass, including the Brightwell BP-2291 figures (309.00 + 61.80 = 370.80).

**Cause:** the tool took "total" to be the amount due and compared it with the lines alone. Any invoice with VAT therefore came out as a mismatch (309.00 vs 370.80).

**Changes in `seam.py`:**
- The model is now asked for `net`, `vat` and `total` as separate fields. `vat` is 0 when the invoice charges none.
- Code checks the arithmetic, to the cent with no tolerance. The status is `ok` only if the computed lines total equals `net` and `net + vat` equals `total`. Otherwise it is `mismatch` and goes to a clerk.
- The result now includes `net` and `vat`. The line amounts are still computed by code.

**Tests and README:**
- I updated both to match, and added cases for a no-VAT invoice, a mistyped total, lines that differ from net, and VAT left out of the total.
- Existing code that reads the model's JSON answer must now supply `net` and `vat`.

**Behaviour to know about:** if the model leaves out `net` or `vat`, the invoice raises `InvoiceError` and goes to a person rather than being guessed. This follows the charter's rule that a record that can't be checked must not reach the ledger.

I didn't touch the charter. Its currency (ISO 4217) rule is still not in code, but that's unrelated to this request.