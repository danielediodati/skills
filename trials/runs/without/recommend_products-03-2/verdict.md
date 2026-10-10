## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if states_other_price(reason, product["price"]):` `+ reason = ""`: code checks a claim in the reason and overrides the model's text, where the line says claims are not checked. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `"price": product["price"]` still comes from the catalogue. |
| C4 | held | not touched |
| C5 | held | `+ reason = " ".join(reason.split())[:MAX_REASON_CHARS]`: the same one-line cut to 80, only moved above the new check; an empty reason is still kept. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
