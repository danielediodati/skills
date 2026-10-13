# recommend_products charter

Input: shopper's search text, catalogue (list of dicts with id, name, price, rating, in_stock), model (callable prompt -> str), limit (int, default 5)
Output: list of at most `limit` dicts with id, name, price, rating, reason (one line, at most 80 chars), best first

## Free
- Which in-stock products match the search: the model judges relevance, since synonyms and intent cannot be listed in code.
- Order of the picks: the model ranks by fit to the search; code keeps its order and does not re-sort by rating or price.
- How many picks, up to the limit: the model may return fewer when few products fit, rather than padding a weak match.
- Wording and tone of each reason: the model writes it for the customer; code only checks length and line shape, not content or accuracy.

## Constrained
- Query normalisation (trim, collapse whitespace): code makes the prompt input deterministic and keeps a blank search from reaching the model.
- Blank query, or no in-stock products: return [] with no model call; the model cannot invent results from nothing.
- Stock filter: out-of-stock products are removed before the prompt is built, so the model never sees or offers them; a pick of one is also dropped on return as a second guard.
- Prompt product data (id, name, price as 2 decimals, rating): fixed format so the model sees the same facts the code will return.
- Output shape "ID | reason", one per line: fixed in the prompt and parsed in code; anything not matching an ID is ignored, so preamble, bullets and numbering are harmless.
- Valid picks are exact in-stock catalogue IDs, first occurrence only: code rejects invented and repeated IDs, so every result exists and appears once.
- Name, price and rating on the result come from the catalogue, never from the model: the model cannot alter facts shown to the shopper.
- Cap of `limit` picks: enforced by code (break at limit), not only asked for in the prompt; the limit is the contract.
- limit below 1 raises ValueError: a caller error is loud, not silently empty.
- Reason: whitespace collapsed to one line and cut to MAX_REASON_CHARS = 80: the UI strip has room for one short line; 80 is a display contract (README), not a tuning value.
- Missing reason (ID with no "|"): kept with an empty reason, so the product is still shown; code does not reject the pick for lacking prose.
- Unparseable or empty model answer: returns [] with no retry and no fallback to catalogue order; the strip just stays empty rather than showing an unvetted list.
- Model errors (exceptions from the callable): not caught; they propagate to the caller.

## Budget
- Budget: 1 model call per invocation, fixed in code, no retry; 0 calls for blank or no-stock input. No timeout in code (the callable's concern). Context: every in-stock product goes into one prompt with no size cap, so prompt length grows with catalogue size. The 5-pick default is a caller-facing default and may be raised; the 80-char reason cap is not a budget.
