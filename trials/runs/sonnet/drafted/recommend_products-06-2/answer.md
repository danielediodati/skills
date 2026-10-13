I changed the prompt so the model is told to give every product a reason. That makes blank reasons less likely, but it does not guarantee they never appear. The 14 local tests pass; I made no model calls, so I haven't seen it work on the "wireless headphones" search.

**What changed**
- **`seam.py`:** the prompt now says every line must carry a reason written for this search. It should explain why a product is worth attention even when it isn't an exact match, such as wired earbuds or a cable shown for "wireless headphones". If the model can't give a reason for a product, it should leave that product out.
- **`test.py`:** one new test checks that the prompt carries this instruction.

**What I did not change**
The charter lists "a pick with no reason gets `""` and is still kept" as a constrained rule, and says the UI must cope with an empty reason. A hard guarantee would mean moving that line, and only you can decide that. The options are:
1. **Drop picks that have no reason.** The strip never shows a blank, but a relevant product can silently disappear, and a strip of three could become one.
2. **Retry the model for blanks.** This breaks the "one call per request, no retry" budget, so it doubles cost and latency on those searches.
3. **Fill in a fixed fallback reason** (for example "Related to your search"). The strip always looks complete, but the text is generic, and a shopper seeing wired earbuds with that line would still wonder why.
4. **Keep it as is and have the UI handle empty reasons.** The card could collapse the gap, or the strip could hide products with no reason.

I'd go with option 1, plus the prompt change already made. Of the four, it's the only one that guarantees "every product has a reason a shopper can read" at no extra cost, and the prompt now tells the model to leave out what it can't explain.

If you want to confirm the prompt fix first, I can run the "wireless headphones" search against the real model. Before any paid call I'd need a budget agreed with you for this ticket; a handful of single-call trials should be enough.