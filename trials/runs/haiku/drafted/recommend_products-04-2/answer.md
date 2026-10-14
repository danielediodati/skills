The reason line can still be wrong. I made one change that only reduces the risk, and I could not make the guarantee you asked for without changing a line the charter reserves for you.

**What I changed:** In `seam.py`, the prompt now includes one accuracy criterion: the reason must agree with the list, quote no price or rating that differs from it, and call a product top-rated or cheapest only if its figures show that. I read this as a criterion that informs the model's judgement, not a constraint, so it stays within the Free list. The 13 unit tests pass.

**What I did not do:**
- **No code check on reason text.** A guarantee that the Aria never shows "under 100" needs code to check reasons after the model, and the charter lists "No content screening of reasons" as Constrained. Adding that check moves the line. It would buy a deterministic guarantee for prices and ratings: a reason quoting a figure that doesn't match the catalogue would be dropped or rewritten. "Top-rated" and similar standing claims are harder, since code would need a rule for what counts as a standing claim. The charter's own note says this check "belongs in code after the model."
- **No paid calls.** I haven't tested whether the prompt criterion changes what Haiku writes. The Aria error happened even though the price was in the prompt, so the criterion may only lower the rate. Measuring that needs a model run, which needs your approval and a budget.
- **Charter not edited,** as AGENTS.md requires.

**Decisions for you:**
1. Do you want the code check for price and rating figures, which moves the "No content screening" line? If so, do you want standing claims ("top-rated", "cheapest") covered too, or only numbers?
2. Do you want a paid screen of the new prompt to see how often the bad reasons still appear? If yes, tell me the budget for this ticket and I'll show the running total before each call.