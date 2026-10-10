## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `_CURRENCY` only strips a symbol or code next to an amount and discards it; the `currency` field is still the model's answer. |
| F4 | held | not touched |
| F5 | held | `+ return Decimal(("-" if signs == ["-"] else "") + digits)`: negative amounts are still accepted, with a leading or trailing minus. |
| F6 | moved toward code | `+ if isinstance(value, str): return _written_amount(value, label)` also covers quantities, so `+ raise InvoiceError(f"{label} is ambiguous: {text!r}")` now refuses a string quantity such as `"1.250"`, which was read before. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Keys, date format and the at-least-one-line check are not touched; an unreadable amount still raises `InvoiceError(f"{label} is not a number: {text!r}")` naming the field. |
| C2 | held | not touched; the gap stays as it was, since `_CURRENCY` strips text beside amounts and does not check the `currency` field. |
| C3 | held | not touched; the gap stays as it was. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is still computed by code. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
