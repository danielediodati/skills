I made the part of the fix the charter leaves open, but I couldn't finish it. The rest needs a decision from you.

**Why the blank reasons happen:** `seam.py` keeps any pick whose line has no `|` and gives it an empty reason. The charter says this on purpose ("code does not reject the pick for lacking prose"). So when the model returns a bare ID for a product, the card shows nothing under it.

**What I changed:** one sentence in the prompt in `seam.py`, saying every line must have its reason after the `|`. The output format is unchanged, and the reason wording stays with the model, which the charter leaves free. The 13 unit tests still pass.

**What I didn't do, and why:** every code-side fix moves a line in the charter:
- **Fill in a generic reason in code** when one is missing: code would be writing the shopper-facing text, which the charter gives to the model.
- **Drop picks with no reason:** the charter says code must not reject a pick for lacking prose. This is the alternative you suggested for the strip.
- **Retry the model when a reason is missing:** the charter fixes the budget at one model call per search, with no retry.
- **Filter blank cards out in the results page:** this avoids the seam, but it works around the same contract, so I'd rather you make that call.

**Not verified:** I can't tell from here whether the prompt change fixes the real output. Checking it needs paid model calls. Before I run any, I need a spending budget for this ticket from you, and I'll then report the running total against it.

**Your decision:** tell me which line you're willing to move, if any, and what budget to set for a verification run. I haven't edited the charter, and nothing is committed.