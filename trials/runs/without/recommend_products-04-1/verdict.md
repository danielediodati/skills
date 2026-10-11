## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: a pick whose reason is blanked stays in the strip, so the count is still the model's. |
| F4 | moved toward code | `+ if not _reason_is_supported(pick["reason"], product, strip): pick["reason"] = ""` overrides the model's reason where the line says claims "are not checked". `+Do not quote prices or ratings in the reason` also narrows what it may say. |
| F5 | held | not touched: the added keyword lists (`COMPARATOR`, `TOP_RATED`, `UNVERIFIABLE`) are English, but the model still chooses the language. |
| C1 | held | not touched: `products=` is still built from every entry in `available`. |
| C2 | held | not touched |
| C3 | held | not touched: `name`, `price` and `rating` are still copied from `available[product_id]`. |
| C4 | held | not touched: no fallback list added. |
| C5 | held | `" ".join(reason.split())[:MAX_REASON_CHARS]` is unchanged. A reason blanked by `+ pick["reason"] = ""` keeps its product, as the line says of an empty reason. |
| C6 | held | not touched: still one `model(...)` call, and the new check does not retry. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per search. |

## Trial

- where: both
- flagged: no
- stopped: no
