Invoices with German, Italian or French number formatting now load with the right figures. The Kessler total `"1.250,00 EUR"` reads as 1250.00, and the Cartiera line `"2.340,50"` reads as 2340.50. All 16 tests pass, including 2 new ones.

**The cause:** `_number` in `seam.py` passed the text straight to `Decimal()`, which only accepts a dot as the decimal point. Any amount with a comma as the decimal separator was refused before it reached the ledger or the clerk's review.

**The fix** is a new `_decimal` helper in `seam.py` that reads the number the way the supplier printed it:
- The last separator is the decimal point, so `1.250,00`, `1,250.00` and `1250,5` all work.
- A separator that repeats (`1.250.000`) or is followed by exactly three digits (`1.250`) is a thousands separator.
- A leading `0` keeps a lone separator as a decimal, so the existing `0.335` test still holds.
- Spaces, non-breaking spaces and currency signs or codes (`€`, `EUR`) are stripped first.
- Anything else still raises the same `... is not a number` error, so "three hundred" still goes to a clerk.

I also added a sentence to `README.md` describing the accepted formats.

**Decision for you:** a lone separator followed by three digits is read as thousands, so `1.250` becomes 1250. That is almost always right for invoice totals, but a UK unit price written as `1.250` would be read 1000 times too large. If you'd rather refuse those cases than guess, it's a one-line change in `_decimal`, at the cost of sending a few more invoices to the clerk.

I did not change the prompt sent to the model. It still asks for the amounts as printed, and the parser handles the formats. Running the tool on real Kessler and Cartiera invoices would confirm the end-to-end result; I only tested the parsing path here.