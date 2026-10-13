I changed the prompt in `seam.py` so the model is told to write every number as a plain decimal. The existing tests and one new test pass, but I haven't run a real model on your Kessler or Cartiera Lombarda invoices.

**Cause:** the prompt never told the model how to write numbers. It copied "1.250,00" straight from the page, and the code only accepts plain decimals, so it refused the invoice.

**Fix:** the prompt now asks for a point as the decimal separator, no thousands separators and no currency symbols, "whatever the invoice's own convention". It gives "1.250,00" and "1,250.00" as examples that both mean 1250.00. The Kessler invoice should now come through with a total of 1250.00, and the Cartiera Lombarda line price as 2340.50.

**What I left alone:** the code still parses numbers strictly. The charter makes reading number formats the model's decision, and the code's parsing is only a safety net. If the model still returns something like "1.250,00", the invoice is refused with the same error rather than guessed at. A code-side locale parser would have taken that decision from the model, and an ambiguous figure like "1.250" would be guessed at instead of read in context.

**One thing to watch:** a wrongly read figure is still caught by the lines-versus-total check, which sends the invoice to a clerk as `mismatch`. The one case it can't catch is when the model misreads the total and the lines the same way.

I added `test_prompt_asks_for_plain_decimals` to `test.py`. I didn't touch the charter.