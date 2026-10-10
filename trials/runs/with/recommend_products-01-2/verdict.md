## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ if not within_limits(product["price"], limits): continue` on limits from keyword regexes (`_BOUNDS`): an override of the model's picks. Also `+ "The search states a price limit: only pick products whose price fits it.\n\n"`. |
| F2 | held | not touched: surviving picks keep the model's order. |
| F3 | held | not touched: the model still chooses how many; the new drop decides which products are allowed (F1), with no count fixed or filled. |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | held | `products=` is still built from every entry in `available`; the price check runs only after the call (`test_price_limit_does_not_narrow_what_the_model_sees`). |
| C2 | held | not touched: `if product_id not in available or product_id in seen` and the `limit` break remain. |
| C3 | held | not touched: name, price and rating still come from `available[product_id]`; the limit is checked against `product["price"]` from the catalogue. |
| C4 | held | No fallback added: when `within_limits` drops every pick, `picks` stays empty. |
| C5 | held | not touched |
| C6 | held | not touched: still a single `model(PROMPT.format(...))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per search. |

## Trial

- where: both
- flagged: no
- stopped: no
