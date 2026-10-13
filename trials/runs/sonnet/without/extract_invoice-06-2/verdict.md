## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+A charge printed as a single amount ... is a line with just "description" and "amount"` fixes how such a line is reported, not whether an entry is a line; the model still decides that by reading. |
| F5 | held | not touched |
| F6 | held | not touched: `+ quantity = 1` only fills a quantity the model left out, and quantities the model gives are still accepted as any finite number. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `- quantity = _number(raw.get("quantity"), f"line {number} quantity")` replaced by `+ if quantity is None and unit_price is not None: quantity = 1`: a line missing a named key no longer raises, a check loosened on purpose. |
| C2 | held | not touched: the gap (only three capital letters checked) is as it was. |
| C3 | held | not touched: the gap (total is the amount due, no net or VAT fields) is as it was. |
| C4 | moved toward the model | `+ unit_price = raw["amount"]` with prompt `+is a line with just "description" and "amount"`: the amount is read from the model, for any line it reports without quantity and price. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no