## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | The model's picks are not altered; added products are marked apart with `+ "filler": True`, not presented as suiting the search. The fill itself is judged under F3 and C4. |
| F2 | held | Model picks keep their order and come first; `+ key=lambda p: p["rating"]` orders only the fillers appended after them. |
| F3 | moved toward code | `+ if len(picks) < limit:` ... `+ for product in spare[:limit - len(picks)]:`: code tops the strip up to `limit`, overriding the model's choice of fewer, or none. |
| F4 | held | The model's reasons are not touched; `+ "reason": "",` applies only to fillers, which the model did not pick. |
| F5 | held | not touched |
| C1 | held | not touched: the prompt still lists every in-stock product, and the filler step runs after the call. |
| C2 | held | `+ (p for p in available.values() if p["id"] not in seen)` and `spare[:limit - len(picks)]`: fillers are real, in stock, each once, within `limit`. |
| C3 | held | `+ "name": product["name"],` `+ "price": product["price"],` `+ "rating": product["rating"],`: filler data comes from the catalogue. |
| C4 | moved toward code | `+ spare = sorted(` ... `+ picks.append({`: with no valid pick the strip is now a best-rated fallback list, where the line says empty with no fallback. |
| C5 | held | The one-line, 80-character cut on model reasons is not touched, and an empty model reason is still kept. |
| C6 | held | not touched: still a single `model(...)` call, no retry. |
| C7 | held | not touched: the blank-search and nothing-in-stock early return, the `limit` error and the marker skipping are unchanged. |
| B1 | held | not touched: one model call per search. |

## Trial

- where: code
- flagged: no
- stopped: no
