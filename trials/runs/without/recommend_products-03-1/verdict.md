## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: a pick whose reason is blanked stays in the strip, so the count is unchanged. |
| F4 | moved toward code | `+ if _quotes_other_price(reason, product["price"]): reason = ""`: code checks a claim in the reason and overrides the model's text, where the line says claims "are not checked". |
| F5 | held | not touched: the `_PRICE_MENTIONS` patterns use English words but do not fix the language of the reason. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `"price": product["price"]` still comes from the catalogue. |
| C4 | held | not touched |
| C5 | held | `+ reason = " ".join(reason.split())[:MAX_REASON_CHARS]`: still one line cut to 80, and the blanked reason is kept with its product. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
