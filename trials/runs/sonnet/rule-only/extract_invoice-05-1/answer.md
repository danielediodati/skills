Invoices whose own figures add up, VAT included, now get status `ok` and go to the ledger. The Brightwell invoice (309.00 + 61.80 VAT = 370.80) is `ok`. The test suite passes, including new cases for VAT.

**Cause:** the tool compared the sum of the lines (309.00) directly with the amount due (370.80). Any invoice with VAT therefore failed, however correct.

**Changes in `seam.py`:**
- The prompt now asks the model to read the invoice's tax amount (summed over all rates, 0 if none shown), and says line prices are before tax.
- The check, done in code as before, is now `lines_total + tax == total`. The result also carries a `tax` field.
- If the model omits the tax or returns null, it is treated as 0. A VAT invoice read that way becomes a mismatch and goes to a clerk, so a missed tax figure never lets a bad invoice through.
- If the tax value cannot be read as a number, the function raises `InvoiceError`, like the other fields.

I also updated the README and added tests: a VAT invoice that adds up is `ok`; a wrong total with VAT is a mismatch; VAT not included in the total is a mismatch.

**One limit to know about:** the check trusts the VAT amount printed on the invoice and does not verify it against a rate such as 20%. That matches "the invoice's own figures are consistent". A supplier who printed the wrong VAT figure, with a total that includes it, would pass. Checking the VAT against a rate would catch that, but it needs a decision on which rates are acceptable, so I haven't added it.