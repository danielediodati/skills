# recommend_products charter

Input: a shopper's search text, the catalogue (id, name, price, rating, in_stock), a model callable (prompt string in, string out) and `limit` (default 5).
Output: a list of at most `limit` in-stock catalogue products, best first, each with id, name, price, rating and a one-line `reason` of at most 80 characters.

## Free
- Which products suit the search: relevance is judgement of meaning (synonyms, intent, "cheap", "for running") that code cannot match with rules; the model sees name, price and rating and may weigh them as it sees fit.
- How many to pick, from none up to `limit`: code does not pad, so fewer, or zero, good matches is a legitimate answer; padding would show irrelevant products.
- The order, best first: the model's order is the ranking; code does not re-sort by rating, price or catalogue position, so the model can trade relevance against quality and price.
- The wording of each reason: what to tell the shopper about a product is writing, tailored to the query; the prompt only asks for one short reason addressed to the customer.

## Constrained
- Which products are candidates: only `in_stock` products are offered to the model and only they can be returned (checked before the call and again on the answer); recommending something that cannot be bought is a failure the model must not be able to cause.
- Whether the model is called: a blank query (after whitespace normalisation) or nothing in stock returns `[]` with no call; there is nothing to judge and the call would cost money and time.
- Number of calls: exactly one per request, no retry, no second pass, no fallback ranking; keeps latency and cost fixed for a page strip. An unusable answer simply gives `[]`.
- The product data shown: name, price and rating come from the catalogue by ID, never from the model's text; the model cannot misstate a price or rating.
- What counts as a pick: a line whose ID (after stripping a list marker, `-`, `*`, `•`, `1.` or `1)`, and before the first `|`) exactly matches an in-stock ID. Case-sensitive, no fuzzy matching; invented IDs, chatter and malformed lines are skipped rather than guessed at. Cheap and checkable; loosening it risks showing the wrong product.
- Duplicates: an ID counts once, at its first position and with its first reason.
- The cap: `limit` is enforced in code, whatever the model returned; the prompt asks for up to `limit`, but the page layout cannot depend on the model obeying it. `limit < 1` raises `ValueError`.
- The answer format: one `ID | reason` per line, fixed in the prompt and the parser. It is the contract between prompt and code; change the two together.
- The reason's shape: whitespace collapsed to one line and hard-cut at `MAX_REASON_CHARS` = 80 (no ellipsis, may cut mid-word); it is a display limit of the UI, so it is the constraint itself, not a budget. A missing reason becomes `""` and the product is still returned.
- Query handling: whitespace is normalised before use; the query is otherwise passed to the model as typed, with no length cap or escaping.
- Output fields: exactly id, name, price, rating, reason; `in_stock` is not returned.

## Target and budget
- Budget: one model call per request; no timeout or retry in the seam.
- Context: every in-stock product is listed in the prompt, with no cap or pre-filtering. This works for a small catalogue; its size is today's limit, and a large catalogue would need candidate selection in code before the call, which would be a move of the line and must be decided by a person.
- Latency and cost scale with the in-stock catalogue size and with `limit`.
- Reliability target: the output is always valid (real, in stock, unique, within `limit`, reason within 80 characters) whatever the model returns; only relevance and the order depend on the model.
