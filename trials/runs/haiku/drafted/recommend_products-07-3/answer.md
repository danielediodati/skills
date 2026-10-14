The strip should now be able to come back empty for "kettle", but I haven't confirmed that against the real model yet. The 14 unit tests pass.

**What was wrong:** the prompt told the model to "Pick up to N products ... that best match the search", and it never said that picking none was allowed. So the model filled the strip with the closest items it had, such as headphones, a cable and earbuds for "kettle", each with a generic reason.

**What I changed** (`seam.py`, the prompt only):
- It now asks for products that "genuinely suit the search", and says a loosely related product does not suit.
- It says that if none suits, the model should answer with nothing.

The code still does nothing extra. I didn't add keyword matching or a score cut-off. The charter lists relevance judgement as the model's call, so code deciding it would move the line. The charter's existing rules still apply: picks are checked against in-stock IDs, the limit is enforced in code, and the page shows the "no results" message as before.

**Test added** (`test.py`): a check that the prompt contains the "answer with nothing" permission. It guards the wording, not the model's behaviour.

**Not verified:** whether the model now reliably returns nothing for "kettle", misspellings and unstocked brands. That needs live model calls, which cost money. Under `AGENTS.md`, I'd need you to approve a spending budget for this ticket before running them. A small check would be a handful of queries you already see failing (for example "kettle", a misspelt cable search, and an unstocked brand), plus a few searches that should still return products, to confirm the strip still works where it should. The prompt may still let a loose match through sometimes, so that run will show how well it holds.

I didn't edit the charter (`evals/recommend_products/charter.md`). It says relevance and the count are free, which matches this change. If you want a firmer rule, such as a minimum relevance the code enforces, that would move the charter line and is your decision.