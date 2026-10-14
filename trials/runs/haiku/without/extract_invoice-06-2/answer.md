Invoices with single-amount charges now load. The Northgate invoice NF-0718 comes through as two lines, with the delivery at 35.00 (quantity 1), and its total of 285.00 matches the lines, so the status is `ok`. The 16 unit tests pass.

**What changed**

- **`seam.py`**: a line with no quantity is now read as a single charge with quantity 1. Before, `_number` refused it with `line N quantity is missing`.
- **`seam.py` prompt**: the model is told to report a single-amount charge as quantity 1 with unit price equal to the amount. This makes the model's output match the code's expectation.
- **`test.py`**: the old test asserted the refusal you wanted removed, so I replaced it. The new tests cover a lump-sum line, a Northgate-style invoice, and a line with no unit price, which is still refused with a message naming the field.
- **`README.md`**: documents the default.

**Choices I made that you may want to change**

- I defaulted only the quantity. A line with no unit price is still refused, because a charge with no amount can't be checked.
- A line with only an `amount` key and no `unit_price` is still refused. The prompt now asks for `unit_price`, so this should be rare, but it is a gap if the model ignores the prompt.
- If a model drops the quantity from a line that really had one (e.g. "40 brackets at 6.25" with no quantity), the line becomes 6.25 and the total won't match. Such an invoice goes to a clerk as `mismatch` rather than loading wrongly, and the mismatch is the safety check.

I haven't run this against the real Northgate text or a live model. The tests use a fake model, so the prompt change is untested in practice; checking a few real invoices would confirm that the model reports these charges with unit price equal to the amount.