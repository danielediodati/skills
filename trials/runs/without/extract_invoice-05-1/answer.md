Invoices whose own figures are consistent now go straight to the ledger, including ones with VAT. All 18 tests pass, but I haven't run this against real model output.

**Cause:** the tool compared the lines (309.00) to the amount due (370.80), so any invoice with VAT looked like a mismatch.

**Change (`seam.py`):**
- The model is now also asked for the `vat` amount charged, with 0 if the invoice shows none.
- An invoice is `ok` when lines + VAT = total, and `mismatch` otherwise.
- Brightwell BP-2291 works out as 309.00 + 61.80 = 370.80 and goes through.
- A wrong quantity or a mistyped total still lands in the review pile, since the sum no longer matches.
- The result now includes a `vat` field. `lines_total` is unchanged.
- I updated the README and added tests for the VAT case, VAT with a wrong total, missing VAT, and unreadable VAT.

**Behaviours to be aware of:**
- **Missing VAT:** if the `vat` field is missing from the model's answer, it is treated as no VAT. A VAT invoice where the model fails to report the VAT therefore goes to review, which is the safe direction.
- **Unreadable VAT:** a VAT value that isn't a number raises `InvoiceError`, like the other fields.
- **VAT rate not checked:** the tool does not check that VAT is the right percentage of the lines. If a supplier computes VAT wrongly but totals it consistently, the invoice passes. I left that out because rates vary by supplier and item, but it's easy to add if you want it flagged.