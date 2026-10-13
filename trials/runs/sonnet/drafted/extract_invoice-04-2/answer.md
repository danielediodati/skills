I changed the prompt so the model is asked to normalise European-style amounts. I have not yet checked that it actually does this on a real invoice.

**Cause:** the prompt asked for "the amount due" and never said how to write numbers. The model copied "1.250,00" as printed, and the code, correctly strict, refused it.

**Fix (`seam.py`):** the prompt now tells the model to write `quantity`, `unit_price` and `total` as plain digits with a point as the decimal separator, no thousands separator and no currency symbol. It gives examples: "1.250,00" and "1 250,00" become 1250.00, and "2,340.50" becomes 2340.50.

**Code and charter unchanged:**
- The charter lists normalising "1.234,50" into a number as the model's decision, with code only checking the result.
- The strict number check stays as it was. Having code parse "1.250,00" itself would be a guess about what the figure means, and "1.250" is ambiguous between 1,250 and 1.25. The model can tell which from the invoice context.
- Invoices where the model still returns a non-numeric figure keep failing loudly rather than loading a wrong amount.

**Tests:** I added a test that the prompt carries the instruction. The suite passes, 15 tests. It uses a fake model, so it does not prove the real model now returns `1250.00` for the Kessler invoice.

To check that, someone needs to run the Kessler (KW-10482) and Cartiera Lombarda invoices through the real model. That is a paid call, so I haven't made it. If you want it, tell me the budget you're comfortable with for this ticket and which model to use. I'd need the invoice texts too.