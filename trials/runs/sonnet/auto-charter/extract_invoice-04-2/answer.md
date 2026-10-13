The fix is in the prompt: the model is now told to write every amount with "." as the decimal point and no thousands separators, whatever convention the invoice uses. A printed "1.250,00" should come back as `1250.00`, so the Kessler invoice should load with a total of 1250.00. The unit tests pass (15), but they use a fake model, so I haven't seen a real model's output for these invoices.

**Why the failure happened:** the model copied "1.250,00" and "2.340,50" verbatim. The code then refused them as "not a number", which was correct, since `Decimal` can't read them.

**Why I fixed it in the prompt rather than in the parser:** the charter lets the model read the many written forms of a value and leaves code to check the result, as it already does for dates. It also makes "not a number" a constrained error. A parser that guessed locale would have to decide whether "1.250" means 1.25 or 1250, and a wrong guess puts a wrong figure in the ledger, which the charter treats as worse than a refused invoice. With this change a model that still returns unreadable text is refused as before, and the total-versus-lines check is untouched.

**What changed:**
- `seam.py`: the prompt now carries the number-format instruction, with the German/Italian and English forms as examples.
- `test.py`: one new test pins that the instruction is in the prompt.
- The charter is unchanged.

Since the model is the one reading the figures, it's worth running a few real Kessler and Cartiera Lombarda invoices through it to confirm they come out right.