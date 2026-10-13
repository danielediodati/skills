## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the added prompt text concerns the reason, not which products are picked. |
| F2 | held | not touched |
| F3 | held | not touched: a rejected reason is blanked, the pick itself is kept. |
| F4 | moved toward code | `+ if _states_price_or_rating(reason): reason = ""` and `+ Do not mention prices, ratings, or how products compare on price or rating`: code now checks and overrides claims the line says are not checked. |
| F5 | held | not touched: nothing in the prompt or code fixes the language of the reason. |
| C1 | held | not touched: `products=` still lists every in-stock product with price and rating. |
| C2 | held | not touched |
| C3 | held | not touched: `"price": product["price"]` and `"rating": product["rating"]` are unchanged. |
| C4 | held | not touched |
| C5 | held | `+ reason = " ".join(reason.split())` then `"reason": reason[:MAX_REASON_CHARS]`: still one line, cut to 80, and an empty reason is still kept. |
| C6 | held | not touched: still a single `model(...)` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
