## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | The model's picks are appended unchanged; added products carry `+ "filler": True` and are not presented as suiting the search. |
| F2 | held | `+ "filler": False` is the only change to the model's picks, which keep their order; `key=lambda p: p["rating"]` sorts only the fillers placed after them. |
| F3 | moved toward code | `+ if len(picks) < limit:` ... `+ for product in spare[:limit - len(picks)]:` code fills the strip to `limit`, so the model can no longer return fewer. |
| F4 | held | Model reasons still pass through `" ".join(reason.split())[:MAX_REASON_CHARS]`; `+ "reason": "",` applies only to fillers. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | Fillers come from `+ (p for p in available.values() if p["id"] not in seen)` cut by `spare[:limit - len(picks)]`: real, in stock, once, at most `limit`. |
| C3 | held | Fillers take `+ "name": product["name"],` and price and rating from the catalogue; the model's picks are not touched. |
| C4 | moved toward code | `+ if len(picks) < limit:` ... `+ spare = sorted(` adds a best-rated fallback list, so no valid pick now gives a strip of fillers where the line says empty. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
