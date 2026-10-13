I changed the extraction prompt in `seam.py` so the model writes amounts in plain form. I haven't run it against a real model, so I can't confirm the Kessler invoice now comes through with a total of 1250.00. The 16 unit tests pass, but they use a fake model.

**The cause:** the prompt never said how to write numbers, so the model copied the invoice's own notation (`1.250,00`). The code then correctly refused it.

**The change:** the prompt now asks for every quantity, unit price and total as a plain number with a dot as the decimal separator, no thousands separators and no currency symbols. It gives `1.250,00 EUR` → `1250.00` as an example, so the model converts the figures itself.

**What I left alone:** the number check in the code is unchanged. If the model still returns `1.250,00`, the invoice is refused as before. I deliberately did not make the code parse continental notation, because `1.250` could be 1.25 or 1250. A parser guessing between the two would put wrong amounts in the ledger without a warning.

I added two tests. One checks that the prompt carries the instruction. The other confirms `'1.250,00'` is still refused by the code.

Replay the Kessler and Cartiera Lombarda invoices through the real model to confirm. If the model still slips occasionally, the options are a retry, or letting the code accept an unambiguous continental format. Both change who decides what, so that would be your call.