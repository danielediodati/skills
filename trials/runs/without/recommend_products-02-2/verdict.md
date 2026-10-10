## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | The model's picks pass through unchanged and are marked `+ "filler": False,`; the added products are flagged `"filler": True` and not presented as suiting the search (counted under F3 and C4). |
| F2 | held | The model's picks still come first in the model's order; `+ by_rating = sorted(available.values(), key=lambda p: p["rating"], reverse=True)` orders only the flagged fillers after them. |
| F3 | moved toward code | `+ for product in by_rating:` / `+ if len(picks) == limit: break`: code tops the strip up to `limit`, overriding the model's choice to return fewer or none. |
| F4 | held | The model's reason is still `" ".join(reason.split())[:MAX_REASON_CHARS]`; `+ "reason": "",` applies only to fillers, which the model did not pick. |
| F5 | held | not touched |
| C1 | held | not touched: the prompt still lists every in-stock product; `by_rating` is built after the call. |
| C2 | held | Fillers are drawn from `available`, skipped by `+ if product["id"] in seen: continue`, and stop at `+ if len(picks) == limit: break`. |
| C3 | held | Fillers take `+ "name": product["name"],`, `"price"` and `"rating"` from the catalogue; the model's picks are not touched. |
| C4 | moved toward code | `+ # Too few suitable picks: top up with the best-rated in-stock products.`: a fallback list where the line says an empty strip, as `test_unusable_answer_gives_a_strip_of_fillers` confirms. |
| C5 | held | not touched: the model's reasons are still collapsed to one line and cut to 80, and an empty one is kept. |
| C6 | held | not touched: still a single `model(...)` call, and fillers are added without another. |
| C7 | held | not touched: the blank search, nothing in stock, `limit < 1` and list-marker handling are unchanged. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
