## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ if not within_limits(product["price"], limits): continue` with `_BOUNDS` keyword regexes: a keyword match and an override applied to the model's picks. |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | held | Only `+{price_note}Products (ID | name | price | rating out of 5):` is added; `products=` is still built from every `available` product. |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | `+ if not within_limits(product["price"], limits): continue`: dropped picks are not replaced, so no valid pick still gives an empty list. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
