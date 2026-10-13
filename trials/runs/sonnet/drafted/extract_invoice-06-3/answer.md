I changed the prompt so the model reports a single-amount charge as quantity 1 at that amount, but I haven't confirmed it against a real model. The 16 local unit tests pass, and they use a fake model.

**Cause:** the model was returning the delivery line with no quantity, and the code correctly refuses a missing quantity (`line 2 quantity is missing`).

**Change in `seam.py`:**
- The prompt now explains that a delivery charge, setup fee, call-out or annual subscription printed as one amount is a single line, with quantity 1 and that amount as its `unit_price`.
- It is guidance on how to read the invoice. The model still decides what counts as a line and what its figures are.

**Change in `test.py`:**
- A test checks the prompt carries the guidance.
- A test checks the Northgate shape loads as two lines totalling 285.00 with status `ok`, given a model answer in that form.

**Not changed:** the missing-quantity check in code. Defaulting a missing quantity to 1 there would loosen a constraint the charter sets, because a missing value is never guessed. The charter is untouched.

**Not verified:** I haven't tested whether a real model now reads NF-0718, the IT support fee and the artwork setup correctly. That needs a paid run. If you approve one, I suggest a budget of three calls, one per invoice, on the cheapest model first.