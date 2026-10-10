# recommend_products charter

Input: what the shopper typed, the catalogue, and a model
Output: up to `limit` in-stock products, best first, each with catalogue data and a reason of at most 80 characters; or an empty list

The search may state a need ("headphones for running in the rain") rather than a product name. Matching a need to products is why the model is here.

## Free
- Which products suit the search: linking a need to what products do is reading, not matching words.
- Their order: best for this search, not best by rating or price, which a function could sort.
- How many, from none to `limit`: three that fit beat five that fill.
- What each reason says: a good one says how the product meets the need; claims in it are not checked.
- The language of the reason: it is addressed to the shopper.

## Constrained
- The model sees every in-stock product; code does not narrow the catalogue before the call: a keyword pre-filter drops exactly the products a need-based search is after.
- Only real, in-stock ids, each once, at most `limit`: the valid ids are a closed, complete set.
- Name, price and rating come from the catalogue, never from the model: they are facts the shop already holds.
- No valid pick gives an empty strip, with no fallback list: products unrelated to the search are worth less than no strip.
- The reason is one line, cut to 80 characters; an empty reason is kept: the space under the product is fixed, and the right product without a reason beats no product.
- One model call, no retry: the strip sits at the top of the results page.
- The mechanical steps: a blank search or nothing in stock returns an empty list without calling the model, `limit` below 1 is an error, list markers and chatter in the answer are skipped.

## Target and budget
- Budget: one model call per search.
