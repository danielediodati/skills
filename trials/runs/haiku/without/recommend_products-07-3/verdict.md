## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ A product suits the search only if the customer would plausibly want it ... a close variant, or a direct accessory or alternative`: criteria that inform the model's judgement; the model still reads each search and decides. |
| F2 | held | `best first` is unchanged; the model still orders. |
| F3 | held | `+ If no product suits the search, answer with NONE`: the model decides the count, now explicitly including none. |
| F4 | held | `+ saying how the product fits the search`: guidance on the reason's content; the model still writes it and claims stay unchecked. |
| F5 | held | not touched; the reason is still addressed to the customer. |
| C1 | held | not touched; the catalogue is still passed whole, with no pre-filter. |
| C2 | held | not touched; the `product_id not in available or product_id in seen` check and the limit are unchanged. |
| C3 | held | not touched; name, price and rating still come from `available[product_id]`. |
| C4 | held | `NONE` has no `\|`, so it is not in `available` and is skipped, giving `[]`; no fallback list is added. |
| C5 | held | not touched; the `[:MAX_REASON_CHARS]` cut and empty reasons are unchanged. |
| C6 | held | not touched; still a single `model(...)` call with no retry. |
| C7 | held | not touched; the blank/nothing-in-stock early return, the `limit < 1` error and the marker/chatter parsing are unchanged. |
| B1 | held | not touched; still one model call per search. |

## Trial

- where: prompt
- flagged: no
- stopped: no