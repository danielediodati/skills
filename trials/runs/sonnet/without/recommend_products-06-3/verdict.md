## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ picks = [p for p in wanted if p["reason"]]`: code removes a product the model chose, an override on the model's answer. |
| F2 | held | Relative order of the model's picks is kept: `wanted = candidates[:limit]`, later picks only appended after. |
| F3 | moved toward code | `+ if p["reason"]: picks.append(p)` and the drop of reasonless picks: a code rule now sets how many are shown, not the model's count. |
| F4 | held | `+ saying why it is worth their attention for this search` informs the model without fixing what it writes; the reason text is still the model's. |
| F5 | held | `+ ID | one short reason, addressed to the customer,` repeats the existing wording; no language is fixed. |
| C1 | held | First call not touched: still lists every in-stock product. The follow-up's `Products (ID | name)` list is not used for picking. |
| C2 | held | `_parse` keeps `if product_id not in available or product_id in seen`; the cap is kept by `candidates[:limit]` and `+ if len(picks) == limit: break`. |
| C3 | held | not touched: name, price and rating are still read from `available[product_id]` in `_parse`. |
| C4 | held | Backfill draws only on the model's own later picks (`for p in candidates[limit:]`); no fallback list is added. |
| C5 | moved toward code | `+ picks = [p for p in wanted if p["reason"]]` and removed `test_pick_without_a_reason_has_an_empty_one`: a rule added where the line says an empty reason is kept. |
| C6 | moved toward the model | `+ followup = model(REASON_PROMPT.format(` : a second model call, a retry for missing reasons, where the line allows one call and no retry. |
| C7 | held | not touched: blank search, nothing in stock and `limit < 1` are unchanged; `LIST_MARKER.sub` still runs in `_parse`. |
| B1 | moved toward the model | `+ followup = model(REASON_PROMPT.format(` : up to two calls per search; the line sets one and does not say the cap may be raised. |

## Trial

- where: both
- flagged: no
- stopped: no