## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ ... Lines are net of tax.`: a general rule from the request that the model still applies by reading each invoice. Which entries are lines (delivery, discounts) stays its call. |
| F5 | held | not touched; `_cents(_number(raw_tax, "tax"))` sets no sign rule. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: the prompt names a `"tax"` key, but an answer without it passes as 0 instead of raising `InvoiceError`. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: tax is its own field and code checks the arithmetic with the total. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch"`: still exact equality to the cent in code, no tolerance, otherwise `mismatch`. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
