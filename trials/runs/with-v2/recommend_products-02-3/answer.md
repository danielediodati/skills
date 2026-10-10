I haven't changed anything: this request can't be met without moving two lines the charter (`evals/recommend_products/charter.md`) draws, and only you can move those.

**What the request collides with**
- **No fallback list.** The charter's constrained section says "No valid pick gives an empty strip, with no fallback list: products unrelated to the search are worth less than no strip." Your completely empty strip is this rule working as written. Filling it with the best-rated in-stock products is exactly the fallback list the charter forbids.
- **How many.** "How many, from none to `limit`: three that fit beat five that fill" is listed as free for the model. Topping up to five in code takes that decision away from the model.

I also didn't nudge the prompt towards "always return five". That would dictate the count and move the same line from the other side.

**What moving the lines would buy**
- A full strip whenever at least `limit` products are in stock, with real recommendations first and best-rated fillers after.
- In the code I'd tag each item, for example `"filler": True`, so the page can show "You may also like" and drop the reason line. The tests and README would be updated to match.
- The cost is that for a search the model judged to have no good match, the strip would show unrelated best-sellers instead of nothing, and the strip would never again show fewer than five.

**A different question you may want to raise**
The `usb-c cable` case is a different problem. Forty matching cables were in stock and the model returned two. That's the model's free decision, but it looks like under-selection rather than "three that fit beat five that fill". If the real complaint is that the model is too stingy when many products fit, there is a charter-compatible route: you tell me, or I check with real model output, whether the prompt makes the model think it should be selective. Criteria that inform its judgement are allowed; a quota is not.

**Decision for you**
Should the charter be amended to allow a rated top-up of the strip? If so:
- Do you want it unconditional, or only when the model returned at least one pick?
- Should the empty-strip rule change?

Once you've changed the charter, I'll implement it.