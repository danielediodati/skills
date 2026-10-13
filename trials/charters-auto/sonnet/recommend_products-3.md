# recommend_products charter

Input: a shopper's search text, a catalogue (id, name, price, rating, in_stock), a model callable, and a limit (default 5).
Output: a list of at most `limit` in-stock catalogue products, best first, each with id, name, price, rating and a one-line reason.

## Free
- Which products suit the search: the model judges relevance from the query and product names/prices/ratings; matching free-text intent to a catalogue is what code cannot do.
- How many to return, from zero up to `limit`: the prompt says "up to", so the model may return fewer when little fits; code does not pad.
- The order of the picks: the model ranks "best first" and code keeps its order; ranking by fit to the search is a judgement, not a sort key (code does not re-sort by rating or price).
- The wording of each reason: the model writes it, addressed to the customer, with only the length and shape fixed by code.
- How to weigh price and rating against the query: the prompt gives them as context only; no rule turns them into a filter or score.

## Constrained
- Blank or whitespace-only query returns `[]` with no model call: nothing to match, so a call would cost money and could only invent results.
- Query whitespace is collapsed before it reaches the prompt: keeps the prompt stable and the blank check reliable.
- Only `in_stock` products are shown to the model and only they can be returned: stock is a fact the shop owns, and recommending something unbuyable is a visible failure; filtering before the prompt also saves context and stops the model choosing them.
- No in-stock products returns `[]` with no model call: nothing to choose from, so the call is wasted.
- `limit < 1` raises `ValueError`: a caller bug is refused loudly, not turned into an empty strip.
- The `limit` is both told to the model and enforced in code (stop at `limit`): the prompt is a request, the cut is the guarantee.
- Model output format is `ID | reason` per line, parsed by code: keeps the answer cheap to check; list markers (`-`, `*`, `•`, `1.`, `1)`) are stripped and lines that are not a known ID (chatter, headings) are skipped rather than failing.
- An ID not among the in-stock products is dropped silently: the model may invent or pick out-of-stock IDs, so only real IDs count and the seam never fails on them.
- A repeated ID counts once, first occurrence wins (its reason and position): no product appears twice in the strip.
- Name, price and rating come from the catalogue, never from the model's text: the model cannot misquote a price or rename a product.
- Reason is whitespace-collapsed to one line and cut at `MAX_REASON_CHARS` = 80: the shop's layout needs one short line; the cut is a hard limit of the display, not a budget (a plain truncation, no ellipsis or re-ask).
- A pick with no reason is kept with `reason` `""`: a valid product is worth showing even if the explanation is missing; code does not call the model again or invent text.
- If the model returns nothing usable, the result is `[]`: no fallback ranking, no retry, no default products.
- Price is shown to the model with two decimals; the catalogue is listed in catalogue order with the fields id, name, price, rating: the prompt format is fixed in code and the tests check it.

## Budget
- Budget: exactly one model call per request, none when the query is blank or nothing is in stock; no retry. The prompt carries the whole in-stock catalogue, so context grows with catalogue size and the seam assumes the catalogue fits in one prompt; a larger one would need a pre-filter, which is a decision to take explicitly.
- Budget: `limit` default 5 is the caller's choice and only today's value; the 80-character reason cap is tied to the display.
