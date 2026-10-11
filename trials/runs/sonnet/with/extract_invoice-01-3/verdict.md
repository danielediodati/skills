## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ _CURRENCY = r"(?:[A-Za-z]{3}\|Fr\.\|[$£€¥₹₽₩₪₺])"` only strips a symbol or code beside an amount; the `currency` field is still the model's answer. |
| F4 | held | not touched |
| F5 | held | `+ if (match["sign1"] or match["sign2"]) in ("-", "−"): number = -number`: negative amounts still pass through as the model gave them. |
| F6 | moved toward code | `+ raise InvoiceError(f"{label} is ambiguous, thousands or decimals: {text!r}")` runs on quantities too: a string quantity such as `"1.250"` (kilos, metres), accepted before, is now refused by a code rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ if isinstance(value, str): number = _written_amount(value, label)`: amounts are still checked by code, and an unreadable one still raises `InvoiceError` naming the field. |
| C2 | held | not touched: the `currency` field is still checked only as three capital letters, so the gap is as it was. |
| C3 | held | not touched: the gap is as it was. |
| C4 | held | not touched: `amount` is still `_cents(quantity * unit_price)`, computed by code. |
| C5 | held | not touched |
| C6 | held | not touched: the parsing is in `_number`, with no second call, retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
