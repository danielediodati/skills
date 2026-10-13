# recommend_products charter

Input: a shopper's search text, the catalogue (id, name, price, rating, in_stock per product), a model callable (prompt -> string), and `limit` (default 5).
Output: a list of at most `limit` in-stock catalogue products, best first, each with id, name, price, rating and a one-line `reason` of at most 80 characters.

## Free
- Which products suit the search: relevance is a judgement about language and intent that code cannot match; the prompt asks the model to match the search to name, price and rating.
- How many to return, from none up to `limit`: the prompt says "up to", so the model may return fewer when little fits. Code only caps it.
- The order of the results: "best first" is the model's ranking, and code keeps it as given.
- The wording and content of each reason: it is written for the customer and depends on the query and the product; code only trims it.
- How price and rating weigh against name fit: the prompt gives no formula, so the model trades them off per search.

## Constrained
- Blank or whitespace-only search returns `[]` without calling the model: there is nothing to match, and a call would cost money for no answer.
- A catalogue with nothing in stock returns `[]` without calling the model: nothing can be shown, so the call would be wasted.
- Query whitespace is collapsed before use: the model sees a normalised search, and blankness is judged on that.
- Only in-stock products are shown to the model: it cannot recommend what the shop cannot sell, and out-of-stock items stay out of the prompt. Today's rule is the `in_stock` flag, nothing more.
- Picks whose ID is not in the offered list are dropped (invented, out-of-stock, or chatter lines): the model is not trusted to give real IDs, and a shown product must exist and be buyable.
- A repeated ID counts once, at its first position and with its first reason: the strip must not show a product twice.
- Name, price and rating come from the catalogue, never from the model's text: the model may misquote them, and the shopper must see true values.
- The result is cut at `limit`, in model order: the strip has fixed room. `limit` is the caller's number, not fixed here.
- `limit` below 1 raises `ValueError`: it is a caller bug, not something to answer around.
- Reason is whitespace-collapsed to one line and cut at 80 characters (`MAX_REASON_CHARS`): the UI shows one line under the product. The cut is hard, with no ellipsis and no word boundary. 80 is a display limit and may change with the layout.
- A pick with no reason gets `""`, and is still kept: a valid product is not lost because the model's explanation is missing. The UI must cope with an empty reason.
- Answer format is one `ID | reason` per line, with leading bullets or numbers tolerated and other lines ignored: code parses it simply and does not ask the model for JSON. A line with an ID that does not parse is dropped silently.
- An answer with no valid picks gives `[]`: there is no fallback ranking, no retry and no filling up from the catalogue by rating or price. Falling back to such a ranking would show products the model did not judge relevant.
- The model is called once per request, with no retry and no validation pass: this keeps cost and latency to one call.
- Model errors are not caught: they propagate to the caller, who owns the handling.

## Budget
- Budget: one model call per request, none for a blank search or an empty stock. The whole in-stock catalogue goes into the prompt, so prompt size grows with catalogue size and there is no pre-filtering or cap. That is today's design, which fits a small catalogue and would need a retrieval step before the model for a large one.
