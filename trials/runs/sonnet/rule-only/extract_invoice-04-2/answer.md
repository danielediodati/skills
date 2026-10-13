I changed the prompt so the model writes amounts in plain dot-decimal form. I haven't run it against the real model, so I can't confirm the Kessler invoice now loads with 1250.00. The tests only check that the instruction reaches the model, and they pass.

**Cause:** the prompt never said how to write amounts, so the model copied the page ("1.250,00") and the code correctly refused it as not a number.

**Change (`seam.py`, `PROMPT`):** it now tells the model that suppliers use different national number styles, to read each amount as the supplier means it, and to return quantities, unit prices and totals as plain numbers with a dot decimal and no thousands separator (e.g. `1250.00`). I also added a test (`test.py`) that the instruction is in the prompt.

**Code unchanged:** the number check in code stays strict. A string like `1.250` is ambiguous (1.25 or 1250) without knowing the supplier's locale. Having code guess would risk a wrong figure reaching the ledger, whereas the model can see the surrounding invoice and read it. The existing total-versus-lines check still sends any disagreement to a clerk.

**Possible follow-up:** if the model still sometimes returns a locale-formatted string, you could have code accept unambiguous cases such as "1.250,00", where both separators appear. That would loosen the code-side check, so it's your call; I haven't done it.