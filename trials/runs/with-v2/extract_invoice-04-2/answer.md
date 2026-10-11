I fixed this in the prompt in `seam.py`, so I haven't confirmed that a real model now returns `1250.00` for the Kessler invoice. The 16 existing and new tests pass, but they use a fake model.

**Cause:** the model was copying the amounts as printed (`"1.250,00"`), and the code correctly refused to treat that as a number.

**Change:** the prompt now tells the model that suppliers write numbers in their own country's style. It must read each figure the way the supplier meant it and write quantity, unit price and total as a plain decimal such as `1250.00`.

**Why the prompt and not a parser in code:** a parser would have to guess what `1.250` means, which could be 1250 or 1.25, and a wrong guess would put a wrong amount into the ledger. The model can see the supplier's country, the currency and the rest of the invoice, so it is better placed to decide. The checks in code are unchanged. A figure the model still returns in continental notation is refused with the same "is not a number" error, and the line-total check against the invoice total is untouched. This matches the charter, which keeps reading the invoice with the model and the arithmetic in code.

**Tests added:** one checks that the prompt carries the instruction. The other checks that code does not guess continental notation, so `"1.250,00"` still raises.

To confirm it works, run a few real German and Italian invoices, Kessler KW-10482 and Cartiera Lombarda first, through the real model.