# recommend_products charter

Input: a shopper's search text, the catalogue (id, name, price, rating, in_stock), a model callable (prompt -> string), and a `limit` (default 5).
Output: a list of at most `limit` products, best first, each with catalogue `id`, `name`, `price`, `rating` plus a one-line `reason` of at most 80 characters.

## Free
- Which products suit the search: relevance is a judgement about meaning (synonyms, intent, accessories vs. main items) that code cannot encode; the prompt gives no filter or scoring rule.
- How many to return, from zero up to `limit`: the model may return fewer when little matches; code never pads the list or demands a minimum.
- The order of the picks: "best first" is the model's call, and code keeps its order as is (no re-sort by rating or price).
- The wording and content of each reason: it is written for the customer, in the model's own words and language; code only checks its length and shape.
- How to weigh name, price and rating against the query: the model sees all three, and no rule says which wins.

## Constrained
- Blank query (after whitespace normalisation) returns `[]` with no model call: nothing to match, and a call would cost money for a guaranteed useless answer.
- Query whitespace is collapsed before it enters the prompt: keeps the prompt single-line and stable; the query is otherwise passed in as typed.
- Only in-stock products are shown to the model and only in-stock products can come back: an out-of-stock recommendation is a broken promise to the shopper, so this is never left to the model (it is enforced twice, in the offer and in the check on the answer).
- Nothing in stock returns `[]` with no model call: same reason as the blank query.
- `limit < 1` raises `ValueError`: a caller bug is refused loudly, not turned into an empty strip. The limit is also told to the model but enforced in code, which stops reading at `limit` picks.
- Every returned id must exist in the catalogue and be new: the model may invent or repeat IDs, so those lines are dropped silently; the first occurrence (and its reason) wins. Matching is exact and case-sensitive.
- Name, price and rating come from the catalogue, never from the model's text: shown facts must be true, so the model cannot alter them.
- Answer format is `ID | reason`, one product per line, parsed leniently: list markers (`-`, `*`, `•`, `1.`, `1)`) are stripped and lines that do not start with a known id (chatter, blanks) are ignored; the reason is everything after the first `|`. Leniency keeps a slightly off-format answer usable; the output is still strict.
- Reason is whitespace-collapsed to one line and hard-cut to 80 characters (`MAX_REASON_CHARS`, no ellipsis): it sits under a product in a fixed layout. The 80 is a display limit stated in the README, not a budget. A pick with no reason is kept with `""`, not dropped: the product is valid even if its explanation is missing.
- No validation of the reason's content (relevance, language, truthfulness) and no retry or fallback ranking: if the model returns nothing usable, the result is `[]`, and a model exception propagates to the caller. This is today's behaviour, not a stated rule.
- Prompt shape is fixed: one call, the full in-stock catalogue listed as `ID | name | price (2 decimals) | rating`, the instruction wording and answer format.

## Budget
- Budget: one model call per request, none when the query is blank or nothing is in stock. No retries.
- Budget: context grows with the whole in-stock catalogue, since every in-stock product is sent with no cap or pre-filter. Fine for a small catalogue; a large one would need a code-side pre-filter, which would move relevance (a Free decision) partly into code, so that needs a decision first.
- Budget: `limit` default 5 is a caller-side default, not a fixed constraint.
