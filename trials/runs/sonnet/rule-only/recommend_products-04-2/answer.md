I made a prompt-only change, which makes wrong reasons less likely but does not guarantee they never appear. The tests pass (14, including one new test).

**What changed**

The prompt in `seam.py` now tells the model that the reason is shown next to the listed price and rating. Anything it says about price, rating or comparison with other products must agree with the figures in the list, and it should leave a claim out if unsure. The new test only checks that this wording is in the prompt.

**Why it isn't a guarantee**

The reason is free text the model writes, and nothing in code currently checks it against the catalogue. Whether a reason is true is a decision the code leaves to the model today. Making it reliable means moving that line, which is your decision rather than mine. The options:

1. **Code check on the reason.** The code compares any price, rating or "top-rated"/"cheapest"-style claim in the reason against the catalogue. When one disagrees, it blanks the reason or drops the pick.
   - Buys: the Aria can never appear with "under 100".
   - Costs: the code now decides which reasons are acceptable, and a pattern check will miss some phrasings. A product can end up with no reason.
2. **Reasons written by code.** The model only picks and orders products, and the line under each is built from the catalogue figures.
   - Buys: it is correct by construction.
   - Costs: the model no longer writes the reason, so the lines become more generic.
3. **Keep the prompt-only fix.** It costs nothing but offers no guarantee.

Given the consumer-protection concern, I'd choose option 1 with the reason blanked on a mismatch, since the pick itself is still good. Tell me which you want and I'll implement it.