## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Only pick a product if it is what the customer is looking for, or a clear alternative to it.` is a criterion the model applies by reading each search; code still does not decide suitability. |
| F2 | held | not touched; the prompt still says "best first" and the model orders. |
| F3 | held | `+ If no product in the list suits the search, pick none and answer with nothing at all.` lets the model choose from none to `limit`, as the line says. |
| F4 | held | not touched; the reason format instruction is unchanged. |
| F5 | held | not touched; the reason is still "addressed to the customer". |
| C1 | held | not touched; the catalogue is still passed whole to the model, with no pre-filter. |
| C2 | held | not touched; the `available` and `seen` checks and the `limit` break are unchanged. |
| C3 | held | not touched; name, price and rating still come from `available[product_id]`. |
| C4 | held | not touched; no valid pick still returns `[]`, and no fallback was added. |
| C5 | held | not touched; the reason is still collapsed to one line and cut to `MAX_REASON_CHARS`, and an empty reason is kept. |
| C6 | held | not touched; still one call, with no retry. |
| C7 | held | not touched; blank query, nothing in stock, `limit < 1` and list-marker skipping are unchanged. |
| B1 | held | not touched; still one model call per search. |

## Trial

- where: prompt
- flagged: yes
- stopped: no