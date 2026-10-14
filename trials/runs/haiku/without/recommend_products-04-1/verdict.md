## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if PRICE_OR_RATING_CLAIM.search(reason): reason = ""`: code now checks the reason's claims and overrides it, where the line says claims are not checked. The prompt also adds "must not mention any price, rating, number...". |
| F5 | held | not touched; the regex does not choose the language of the reason. |
| C1 | held | not touched; the full in-stock list still goes to the model. |
| C2 | held | not touched |
| C3 | held | not touched; name, price and rating still come from `product`. |
| C4 | held | not touched |
| C5 | held | the cut `[:MAX_REASON_CHARS]` and one-line normalization remain, and an empty reason is still kept. |
| C6 | held | not touched; still one call and no retry. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per search. |

## Trial

- where: both
- flagged: no
- stopped: no