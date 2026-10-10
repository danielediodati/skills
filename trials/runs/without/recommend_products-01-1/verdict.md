## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ if p["in_stock"] and (within is None or within(p["price"]))` with the `_PRICE_BOUNDS` regexes: a keyword rule decides which products cannot suit the search, before the model reads it. |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | moved toward code | `- available = {p["id"]: p for p in catalog if p["in_stock"]}` becomes `+ ... if p["in_stock"] and (within is None or within(p["price"]))`: code narrows the catalogue before the call, so the model no longer sees every in-stock product. |
| C2 | moved toward code | `+ within = price_limits(query)` narrows `available`, so `if product_id not in available` now drops real, in-stock ids too (`test_model_picks_outside_the_limit_are_dropped`): tighter than the line says. |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
