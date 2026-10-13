I changed the prompt so the model writes amounts in plain notation, and the local tests pass (16/16). I have not run it against a real model, so I can't yet say the Kessler invoice now loads with a total of 1250.00.

**Cause:** the prompt never told the model how to write numbers. It copied "1.250,00" straight from the page, and the strict number check in code rejected it.

**Change (`seam.py`, `PROMPT`):**
- The prompt now says invoices use different national number styles.
- It asks for every quantity, unit_price and total as a plain number: full stop as the decimal separator, no thousands separator, no currency symbol.

**Tests (`test.py`):**
- One checks that the instruction reaches the model.
- One confirms an answer that still contains "1.250,00" is refused with `total is not a number`.

**Charter:**
- No line moved, and I did not edit the charter.
- Reading the figures stays with the model, in the same way date and currency normalisation does.
- The code check stays exact and strict, so a figure the model still gets wrong fails visibly instead of being guessed.

**Why not a locale parser in code:** a rule that reads "1.250" as either 1250 or 1.25 would be guessing a value, and that is exactly what the charter forbids. The model can use the surrounding context to decide.

**Checking it for real:** I'd propose a small paid run with a handful of invoices, such as the Kessler and Cartiera Lombarda ones plus a UK, a "1 250,00" and an ambiguous "1.250" case, using the cheapest model first. Nothing has been spent, and we have not agreed a budget. If you want to go ahead, tell me the budget and which model to use.