## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ return [c for c in candidates if c["reason"]][:limit]`: code removes products the model picked as suiting the search and promotes later ones in their place. |
| F2 | held | The relative order of the model's picks is kept: `_parse` still reads lines in order and the final filter preserves it. |
| F3 | moved toward code | `+ return [c for c in candidates if c["reason"]][:limit]` with `- if len(picks) == limit: break`: code now shrinks or refills the count the model chose. |
| F4 | held | `+ why it is worth their attention for this search.` informs the retry, but the model still writes each reason and nothing in it is checked. |
| F5 | held | `+ say in one short sentence, addressed to the customer,` keeps the reason addressed to the shopper; the language is not fixed. |
| C1 | held | not touched: the first call still lists every in-stock product; the retry only lists products already picked. |
| C2 | held | `+ if product_id not in known or product_id in seen:` with `known=available`, and `[:limit]` on the return, still give real in-stock ids, once each, at most `limit`. |
| C3 | held | `+ reasons = {c["id"]: c["reason"] for c in retry}`: only the reason is taken from the retry; name, price and rating still come from the catalogue. |
| C4 | held | not touched: no fallback list was added; no valid pick still gives an empty list. |
| C5 | moved toward code | `+ return [c for c in candidates if c["reason"]][:limit]`: a pick with an empty reason is dropped where the line says it is kept. The one-line, 80-character cut still holds. |
| C6 | moved toward the model | `+ retry = _parse(model(REASON_PROMPT.format(`: a second model call, a retry, where the line allows one call and no retry. |
| C7 | held | not touched: blank search, nothing in stock and `limit < 1` are unchanged; `LIST_MARKER.sub` and the skipping of chatter moved intact into `_parse`. |
| B1 | moved toward the model | `+ retry = _parse(model(REASON_PROMPT.format(`: up to two model calls per search against a budget of one, which the line does not say may be raised. |

## Trial

- where: both
- flagged: no
- stopped: no