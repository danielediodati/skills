I changed the prompt so that continental amounts such as "1.250,00" should now come through as 1250.00. Tests pass, but I have not run it against a real model.

**Cause:** the model passed the supplier's notation straight through ("1.250,00"), and the code rejected it as not a number.

**Fix:** the prompt in `seam.py` now tells the model to write every quantity, unit price and total as a plain decimal number. That means "." as the decimal point, no thousands separator and no currency sign. It gives "1.250,00", "1,250.00" and "1 250,5" as examples.

I did this in the prompt rather than parsing separators in code. A string like "1.250" could mean 1250 or 1.25, and the model can tell which from the supplier's country and the surrounding text. The check in code stays strict. An amount the model still can't normalise is refused as before, not guessed at. Line amounts are still computed by code, and the lines must still add up to the total to the cent.

I added one test in `test.py` that checks the prompt carries this instruction. The existing tests all pass (15 total).

**Please check:** try the Kessler (KW-10482) and Cartiera Lombarda invoices against the real model. The fake model in the tests can't show whether it actually follows the instruction.