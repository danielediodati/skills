I've changed the prompt so the model reports VAT as a line, which should let invoices like Brightwell BP-2291 through. I haven't run it against a real model.

**Cause:** the prompt asked for "lines" and never said that a VAT row is one. The model listed only the goods and delivery (309.00) and reported the amount due (370.80). The check compares the two exactly, so it flagged a mismatch every time an invoice charged VAT.

**Change (`seam.py`):** the prompt now tells the model that every row that adds to or subtracts from the amount due is a line. That covers items, delivery, discounts and tax rows such as VAT. It also tells the model to report figures as printed and not to compute or correct any. With the VAT row included, Brightwell's lines come to 309.00 + 61.80 = 370.80, which equals the amount due, so it is marked `ok`.

**Left alone, on purpose:**
- The status rule is still an exact comparison in code. A wrong quantity or a mistyped total still lands in the review pile, because the figures are reported as printed and then summed by code.
- The charter is unchanged. It already leaves "which rows count as lines, tax rows included" to the model, so this is a prompt fix and not a rule change.

**Tests:** I added three, covering a VAT invoice that is `ok`, a VAT invoice with a wrong total that is a `mismatch`, and a check that the prompt mentions tax rows. All 17 tests pass. These use a fake model, so they confirm the code handles a VAT line correctly but not that a real model will now return one.

**Not done:** to confirm that the real model returns the VAT row, I'd need to run it on a few real invoices, which is paid. If you want that check, tell me the number of invoices and a spending budget for this ticket, and I'll go ahead.