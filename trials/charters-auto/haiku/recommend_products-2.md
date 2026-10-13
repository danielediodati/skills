# recommend_products charter

Input: the shopper's search text, a catalogue of products (`id`, `name`, `price`, `rating`, `in_stock`), a `limit` (default 5), and a `model` callable (prompt string in, string out).
Output: a list of at most `limit` dicts (`id`, `name`, `price`, `rating`, `reason`), best first, each product once, all in stock and present in the catalogue.

## Free
- Which in-stock products match the search: the model judges relevance, including loose matches such as "noise cancelling" to a wireless headphone. Code cannot know what a shopper means.
- Order of the picks: the model ranks them and code keeps its order without re-sorting by rating or price. Ranking is a judgement about fit, not a fixed rule.
- How many picks, up to the limit: the model may return fewer than `limit`, and code does not pad the list. Choosing fewer good matches beats filling the strip with weak ones.
- Wording of each reason: the model writes it, addressed to the customer, so it can respond to the particular search. Code only collapses whitespace and cuts length (see Constrained).
- Whether there is any pick at all: a model answer with no valid lines yields an empty list. Code does not invent a fallback ranking, so the model keeps the decision of "nothing fits".

## Constrained
- Blank search returns `[]` without calling the model: nothing to match, and the call costs money and time. Tight: a hard rule.
- Search text is trimmed and inner whitespace collapsed before use: the model sees one clean line in the prompt, and the blank check is reliable. Tight: a hard rule.
- Only in-stock products are shown to the model, and out-of-stock products are never offered: shoppers must not be sent to unavailable items. Tight: a hard rule.
- A catalogue with nothing in stock returns `[]` without calling the model: same reason as blank search. Tight: a hard rule.
- Fields the model sees are fixed to `id | name | price | rating`, price shown with two decimals: the model needs these to judge, and the description, stock count and other fields stay out of the prompt. Changing this changes what the model can judge. Tight: a design choice, not a limit.
- Prompt wording and the answer format `ID | reason`, one product per line: the parser depends on this exact shape, so the format line in the prompt and the parser must change together. Tight: a hard coupling.
- Picks are only counted if the text before the first `|` (after stripping bullets or numbers such as `1.`, `-`, `•`) is exactly an in-stock catalogue ID: invented or misspelled IDs are dropped, so the model cannot add products. Tight: a hard rule. The match is exact and case-sensitive.
- Lines without a valid ID (chatter, headings, "Enjoy!") are ignored: the model can talk around the format and still produce usable picks. Tight: a hard rule.
- A repeated ID counts once, the first occurrence wins: a product should not appear twice in the strip. Tight: a hard rule.
- A pick with no `|` is accepted with an empty reason: the product is still valid, and the reason is only text. Tight: a default, easy to change.
- Name, price and rating come from the catalogue, never from the model: the model cannot change a price or rating the shopper sees. Tight: a hard rule.
- Count capped at `limit` in code, and `limit` must be at least 1 (else `ValueError`, checked before the blank-search check): the strip has a fixed number of slots and a zero or negative limit is a caller bug. The cap is hard. The default 5 is a display choice that a caller may change.
- Reason is one line, whitespace collapsed, cut to 80 characters by a plain slice (may end mid-word): the reason sits under the product in a fixed-width layout. 80 is a layout limit, tight. Code truncates rather than asking the model to shorten, so no extra call is needed.
- No content screening of reasons: code does not check reason text for tone, claims or unsafe content. This is a gap the charter records, not a decision someone made on purpose; if reasons ever need review, that check belongs in code after the model.
- Exactly one model call per search, with no retry, no timeout and no fallback: a failure from the model propagates to the caller. Tight: a design choice; a retry would change cost and latency.
- Full in-stock catalogue sent in every prompt, with no cap on its size: the code does not truncate or pre-filter by query. Tight: unbounded today, a known scaling limit.

## Budget
- Budget: 1 model call per search that has a non-blank query and at least one in-stock product; 0 calls otherwise. No token cap, timeout or retry is set in code. Prompt size grows with the in-stock catalogue, which is not capped. The `limit` default of 5 is a display size, not a cost budget.
