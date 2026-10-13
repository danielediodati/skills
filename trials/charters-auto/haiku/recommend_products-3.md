# recommend_products charter

Input: the shopper's search text, the catalogue (dicts with id, name, price, rating, in_stock), a model callable (prompt in, string out) and a limit (default 5).
Output: a list of at most `limit` dicts with id, name, price, rating and reason (at most 80 characters), best first, each product once.

## Free
- Which products match the search: the model judges relevance from the query and the in-stock list, since matching intent is what the prompt asks it to do.
- How many products to pick, up to the limit: the model may pick fewer when few fit; code never pads the list to the limit.
- Order of the picks: the model ranks them, and code keeps its order, because "best first" is a judgement of fit.
- Wording of each reason: the model writes it for the customer, and code only collapses whitespace and cuts it to 80 characters.

## Constrained
- Blank or whitespace-only query returns [] without calling the model: nothing to match, and a call would be wasted.
- Catalogue with nothing in stock returns [] without calling the model: same reason as above.
- `limit` below 1 raises ValueError: a zero or negative limit has no meaningful result and would hide a caller bug.
- Query is normalised to single-spaced text before it reaches the prompt: keeps the prompt clean and the test for it stable; the model does not see raw spacing.
- Only in-stock products are offered to the model: the model cannot recommend what the shop cannot sell.
- Product name, price (2 decimals) and rating are taken from the catalogue, never from the model: the shopper must see true data, and the model only chooses IDs and writes reasons.
- Each pick must be an ID present in the in-stock catalogue, else it is dropped silently: blocks invented or out-of-stock products from reaching the shopper.
- A repeated ID counts once, keeping its first occurrence: avoids duplicate tiles in the strip.
- Each line is read as `ID | reason`, with list markers and surrounding chatter ignored: the output format is fixed so parsing is deterministic; anything not matching a real ID is discarded.
- A line without a reason is kept with reason "": the product is still valid, only its explanation is missing.
- Reason is one line, at most 80 characters, truncated not rewritten: the strip has fixed space under each product.
- Result is capped at `limit`, enforced in code, not only asked of the model: the strip's layout depends on it.
- Model output that yields no valid IDs returns [] with no retry or error: the strip simply stays empty rather than breaking the results page.
- Exceptions raised by the model callable propagate to the caller: the caller owns retry and fallback policy.
- Default limit of 5: a UI choice for the strip, adjustable by callers; the cap itself is the constraint, the number is today's value.

## Budget
- Budget: exactly one model call per invocation, no retry; no timeout or token cap in code (the callable owns those); prompt size grows with the number of in-stock products, with no cap on catalogue size; the default limit of 5 is a UI value, not a cost cap.
