I changed the prompt, but I couldn't make every product show a reason in code. Making that guarantee means moving a line in the charter, which I'm not allowed to do.

**What's blocking it:** Line 22 of `evals/recommend_products/charter.md` is constrained: "A line without a reason is kept with reason `""`". Line 30 is also constrained: one model call per invocation, no retry. So the three ways to guarantee a reason all move a line:
- **Drop picks with no reason.** This is your second option, and it's a clean fix for the strip. It changes line 22.
- **Fill in a default reason** such as "Matches your search". This changes line 22 and takes the wording away from the model (line 10).
- **Retry the model** when a reason is missing. This changes line 30.

**What I changed:** `seam.py` now tells the model, in the prompt, that every line must have a reason after the `|`. The output format is the one the charter already fixes, so no line moved. The unit tests pass (13 of 13).

**What I haven't verified:** I haven't run the model, so I don't know whether the prompt change stops the blank reasons. A real check needs paid calls, and I haven't agreed a spending budget with you yet. A trial could be a few searches, including "wireless headphones", run through the real model. Tell me the budget and I'll run it.

**Decision for you:** Do you want to move line 22 so that reason-less picks are dropped? That would give the strip only products with a reason, but it may show fewer than five. If you want to keep the charter as it is, the prompt change is the only lever I can pull from here, and it may only reduce how often the blanks appear.

This folder isn't a git repository, so I didn't commit anything.