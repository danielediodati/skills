I changed the prompt so the model reports amounts as plain decimals, which should let invoices like the Kessler one load with a total of `1250.00`. The 16 tests pass, but they use a fake model, so I haven't seen a real model's output on your invoices.

**Cause:** the model was copying amounts as printed (`1.250,00`), and the code's number check correctly refused them.

**Fix (`seam.py`):** the prompt now tells the model that suppliers use different number conventions and to give every quantity, unit price and total with a dot as the only decimal separator and no thousands separator.

I did this in the prompt rather than parsing locale formats in code because code can't tell whether `1.250` means 1250 or 1.25. The model can, because it sees the invoice's language and country.

**Unchanged:** the number check is as strict as before, so an amount that still comes back as `1.250,00` is refused rather than guessed at, and nothing wrong reaches the ledger. The charter is untouched, and this doesn't move any line in it. The tests I added check that the prompt carries the instruction and that the strict check still holds.

**Next step:** run the Kessler and Cartiera Lombarda invoices through the real model once to confirm it follows the instruction.