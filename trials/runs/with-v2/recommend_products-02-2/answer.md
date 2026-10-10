I haven't changed anything, because this request needs a line in the `recommend_products` charter moved, and only you can do that.

**The conflict**
- The charter makes the count a free model decision: "How many, from none to `limit`: three that fit beat five that fill."
- It also makes "No valid pick gives an empty strip, with no fallback list" a constraint, because "products unrelated to the search are worth less than no strip."
- Padding with the best-rated in-stock products is exactly that fill and fallback. It overrides the model's decision on how many, and it makes the empty strip impossible.

**What I'd build if you move the line**
- Real recommendations stay first, in the model's order, unchanged.
- After them, in-stock products not already picked are added in descending rating order until the strip reaches `limit` or stock runs out. Ties break by catalogue order.
- Every item gets a `filler` boolean, `False` for model picks and `True` for padding, with `reason` empty on fillers. Your UI can then use it for the "You may also like" label.
- The model call, prompt and parsing stay as they are, so it is still one call per search.
- I'd update the README and add tests for partial fill, empty fill, ordering, and no duplicates.

**Decisions for you**
1. Should fillers apply when the model returns nothing at all, so the strip is always full? Your second example (a completely empty strip) suggests yes. That reverses the "no fallback list" constraint outright.
2. Should the charter record that fillers are deliberately unrelated to the search and are labelled as such? I can't edit it, so you would have to.

A narrower alternative that stays inside the charter is to pull the model toward fuller strips, for example by telling it that a strip of five is preferred when enough products are relevant. That only informs its judgement and wouldn't guarantee full rows or fix the empty strip case.

Tell me which way you want to go. If you update the charter, I'll implement the filler version.