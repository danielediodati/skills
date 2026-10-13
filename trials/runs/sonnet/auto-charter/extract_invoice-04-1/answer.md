I changed the prompt so the model writes amounts in plain form. That should let invoices like Kessler's load with a total of 1250.00, but I couldn't confirm it here. The tests use a fake model, so none of them show a real model returning 1250.00 for "1.250,00 EUR".

**The cause:** the prompt never told the model how to write numbers. It copied "1.250,00" straight from the page, and the code correctly refused it as not a number.

**The fix (`seam.py`):** the prompt now asks for every number as plain digits, with a dot as the decimal separator and no thousands separator or currency symbol, whatever convention the invoice uses. It gives "1.250,00" and "1,250.00", both meaning 1250.00, as examples. This is the same arrangement the charter already uses for dates: the model reads the many written forms and code only checks the result.

**What I deliberately did not do:** parse "1.250,00" in code. Code can't tell "1.250" meaning one thousand two hundred and fifty from "1.250" meaning one and a quarter. The charter also makes strict `Decimal` parsing a code-side constraint, so the check that refuses a bad reading is unchanged.

**Tests (`test.py`):** I added two. One checks that the prompt carries the number instruction. The other pins that a continental-format total in the model's answer is still refused with `total is not a number`. All 16 tests pass.

**What still fails:** if the model ignores the instruction and returns "1.250,00" anyway, the invoice is still refused, as before. There is no retry, per the charter. Please try a few real Kessler- and Cartiera-style invoices to see whether the model follows the instruction reliably.