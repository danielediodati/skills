## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the model still picks the products; the first prompt is unchanged. |
| F2 | held | not touched: order still comes from the model's answer order. |
| F3 | moved toward code | `+ return [p for p in picks if p["reason"]]`: code now drops picks the model chose, so the model's count is cut by a reason-presence rule. |
| F4 | moved toward code | `+ If a product is not exactly what was searched for, say what it offers that is relevant instead.` in REASON_PROMPT and `+ return [p for p in picks if p["reason"]]`: the second prompt steers what the reason must say, and a pick without a reason is removed. |
| F5 | held | not touched: the reason prompt still says "addressed to the customer". |
| C1 | held | not touched: the first call still lists every in-stock product. |
| C2 | held | not touched: `_parse` keeps the `available` and `seen` checks, and the `limit` cap is still applied in the picks loop. |
| C3 | moved toward the model | `+ products="\n".join(f"{p['id']} | {p['name']}" ...)` and `+ reasons.get(p["id"], "")`: the reason now comes from a second model answer, and name, price and rating still come from the catalogue, so the line holds. The only change is a new source for the reason. |
| C4 | held | not touched: no fallback list; an empty result is still returned when there are no valid picks. |
| C5 | moved toward code | `+ return [p for p in picks if p["reason"]]` and README `Every returned product has a non-empty reason`: the line says an empty reason is kept, and code now drops such products. |
| C6 | moved toward the model | `+ answer = model(REASON_PROMPT.format(` : a second model call, a retry, where the line says one call and no retry. |
| C7 | held | not touched: the blank-search, nothing-in-stock, `limit < 1` and list-marker handling are unchanged, now inside `_parse`. |
| B1 | moved toward the model | `+ answer = model(REASON_PROMPT.format(`: up to two model calls per search where the budget is one. |

## Trial

- where: both
- flagged: yes
- stopped: no