I haven't changed anything yet: this request reverses two things the `recommend_products` charter (`evals/recommend_products/charter.md`) deliberately settles, so it's your call.

**What the charter says today**
- **Free to the model:** "How many, from none to `limit`: three that fit beat five that fill." The two-cable strip is that rule working as designed.
- **Constrained in code:** "No valid pick gives an empty strip, with no fallback list: products unrelated to the search are worth less than no strip." The completely empty strip is this rule.

**What you're asking for**
Top up every strip to `limit` with the best-rated in-stock products not already shown, flagged so the UI can label them "You may also like". That makes the strip always full, and it overrides both rules above.

**How I'd implement it if you confirm**
- After the model picks are parsed, append in-stock products not already picked, sorted by rating descending, until `limit` is reached. Ties would break by catalogue order.
- Each filler gets `"filler": True` and `"reason": ""`. Real picks get `"filler": False`, so the UI can tell them apart without inspecting the reason.
- Real picks stay first, in the model's order. The model call, prompt and parsing don't change.
- The blank-search and nothing-in-stock cases still return an empty list without a model call.
- I'd update the charter in the same change: the "from none to `limit`" and "no fallback list" lines, plus a note that fillers are chosen by code, not the model.
- I'd update the README and the tests: fill-up, ordering, no duplicates, flag values, and fewer in stock than `limit`.

**Two things to decide**
1. **Fillers for off-topic searches.** With this change a search the model finds nothing for gets a strip of top-rated products unrelated to the query. That's what you described, but it's the case the charter was written to avoid. The alternative is to fill only when the model returned at least one pick, which still leaves the empty-strip case you mentioned.
2. **Fewer than `limit` in stock.** I'd return what exists. Say if you want something different.

Tell me to go ahead (and answer 1), and I'll make the code, charter, README and test changes together.