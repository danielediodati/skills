Invoices whose figures are consistent, VAT included, now get `ok` and go to the ledger. The Brightwell invoice (309.00 + 61.80 VAT = 370.80) passes. I added tests for it and the suite passes (18 tests).

**Cause:** the tool compared the sum of the lines (309.00, before VAT) with the amount due (370.80, after VAT). Any invoice charging VAT therefore looked wrong.

**Changes (`seam.py`):**
- The model is now also asked for a `tax` field, the VAT or tax amount shown on the invoice, with 0 if none.
- The check in code is now `lines_total + tax == total`. It is still an exact comparison to the cent, decided in code, not by the model.
- The result includes `tax`, and the README is updated to match.

**What still goes to a clerk:**
- A wrong quantity or price, or a mistyped total, still gives a mismatch.
- If the model leaves `tax` out of an invoice that has VAT, it counts as 0 and the invoice is set aside. Clerks will not see a wrong invoice pass, but a missed VAT figure costs a needless review.
- A `tax` value that isn't a number raises `InvoiceError` naming the field.

**Limitation:** the check relies on the model reading the VAT figure correctly. It does not recompute VAT from the rate, so an invoice whose VAT amount is itself wrong, but whose total is consistent with that wrong VAT, will pass. Recomputing VAT from the rate would be a stricter rule, and it is your decision whether to add it.