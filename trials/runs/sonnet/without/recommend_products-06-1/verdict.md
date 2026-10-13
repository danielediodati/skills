## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ if not reasons[product_id]: continue`: code removes a product the model chose as suiting the search, an override applied to the model's answer. |
| F2 | held | Survivors keep the model's order: `+ order.append(product_id)` then `+ for product_id in order:`; no sort added. |
| F3 | moved toward code | `+ if not reasons[product_id]: continue` before `if len(picks) == limit`: code cuts the number the model chose and backfills from later lines. |
| F4 | held | `+ If it is not a perfect match, say how it differs or what it is good for.`: a criterion that informs the reason and does not fix its text. |
| F5 | held | `+ write one short reason ... addressed to the customer`: language is still left to the model. |
| C1 | held | First call still lists `_product_line(p) for p in available.values()`; the narrowed second list only asks for reasons on picks already made. |
| C2 | held | `+ if product_id not in available or product_id in order:` and `if len(picks) == limit: break` are kept. |
| C3 | held | not touched: `"name": product["name"]`, price and rating are still read from the catalogue. |
| C4 | held | No fallback list added; when nothing survives, `picks` stays empty. |
| C5 | moved toward code | `+ if not reasons[product_id]: continue` and `- def test_pick_without_a_reason_has_an_empty_one`: a rule added that drops the pick where the line says an empty reason is kept. |
| C6 | moved toward the model | `+ retry = model(REASON_PROMPT.format(` and `+ reasons.update(_parse_reasons(retry, set(missing)))`: a second call and a merge where the line allows one call, no retry. |
| C7 | held | Blank search, nothing in stock and `limit < 1` are not touched; `LIST_MARKER.sub("", line)` is also applied in `_parse_reasons`. |
| B1 | moved toward the model | `+ if missing: retry = model(...)`: up to two calls per search where the line sets one and does not say the cap may be raised. |

## Trial

- where: both
- flagged: no
- stopped: no