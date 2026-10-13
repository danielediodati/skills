The prompt in `seam.py` now tells the model to write quantities, unit prices and the total as plain decimals, with a point as the decimal separator and no thousands separators or currency symbols. It uses your Kessler figure as the example: "1.250,00 EUR" is 1250.00.

**Cause:** the model was never asked to normalize numbers, so it often passed "1.250,00" through as printed. The code then correctly refused it, since it only accepts plain decimals.

**Why the prompt:** the charter lists number formatting as a decision the model makes, so I did not add separator parsing in code. A code parser has to guess that "1.250" means 1250 rather than 1.25, which is the kind of misreading that costs money on large invoices.

**Checks:** a new test confirms the prompt carries the instruction, and all 15 tests pass. They use a fake model, so I couldn't confirm that a real model now returns 1250.00 for the Kessler invoice. Please run KW-10482 and the Cartiera Lombarda invoice through the real model to check.

**Not changed:** if the model still returns a non-plain figure, the invoice is rejected rather than guessed, as before. That is the safe failure, and it is the charter's rule.