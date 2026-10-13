## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if not _reason_agrees(pick["reason"], pick, picks):` / `+ pick["reason"] = ""` and prompt `+The reason must not state or hint at a price, a rating`: code checks the claims and overrides the reason, where the line says claims are not checked. |
| F5 | held | not touched: neither the prompt nor the code fixes the language of the reason. |
| C1 | held | not touched: the `products` list is still built from every in-stock product. |
| C2 | held | not touched |
| C3 | held | not touched: `name`, `price` and `rating` in each pick still come from `available[product_id]`. |
| C4 | held | not touched |
| C5 | held | Cut still `[:MAX_REASON_CHARS]`; the added `pick["reason"] = ""` keeps the pick with an empty reason, as the line allows. The content rule is judged under F4. |
| C6 | held | not touched: still a single `model(...)` call, with no retry added. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per search. |

## Trial

- where: both
- flagged: no
- stopped: no
