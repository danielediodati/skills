## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `([^\d\s.,'’+\-−()]+)?` drops a symbol or code beside an amount; the currency still comes from the model's `currency` field. |
| F4 | held | not touched |
| F5 | held | `negative = negative or bool(signs and signs[0] in "-−")`: negatives are still accepted, now in more written forms (`(12.50)`, `€ -12,50`); none is refused or overridden. |
| F6 | held | `_number` also serves quantities, and `"12,5": "12.5"` is still read as a non-integer; no whole-number rule added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ if number is None or not number.is_finite(): raise InvoiceError(f"{label} is not a number: {value!r}")`: an amount code cannot read one way still raises, naming the field; keys, date and lines checks not touched. |
| C2 | held | not touched: the currency check is still three capital letters, so the gap is as it was. |
| C3 | held | not touched: the total is still the amount due, with no net or VAT fields, so the gap is as it was. |
| C4 | held | not touched: `_cents(quantity * unit_price)` is unchanged; `_written_amount` only parses the unit price and quantity the model reports. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged, with no tolerance added. |
| C6 | held | not touched: `+ number = _written_amount(str(value))` is a second parse in code, not a second call or a fallback value. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
