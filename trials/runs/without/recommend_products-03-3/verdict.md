## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if _states_other_price(reason, product["price"]):` / `+ reason = ""`: code checks a claim in the reason and overrides the model's text, where the line says claims are not checked. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `"price": product["price"]` is unchanged, so the name, price and rating fields still come from the catalogue. |
| C4 | held | not touched |
| C5 | held | `+ reason = " ".join(reason.split())[:MAX_REASON_CHARS]`: same one-line cut to 80, only moved up; a blanked reason is kept with its product. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
