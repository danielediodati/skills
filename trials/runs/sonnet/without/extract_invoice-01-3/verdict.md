## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `c.isalpha() or unicodedata.category(c) == "Sc"` only strips symbols and codes from amounts; the `currency` field is still the model's answer. |
| F4 | held | not touched |
| F5 | held | `sign, core = core[0], trim(core[1:])` keeps the sign; `"-£5.00"` reads as `-5.00`, and negative JSON numbers pass as before. |
| F6 | moved toward code | `+ if len(right) == 3 and 1 <= len(left) <= 3 and not left.startswith("0"): raise InvoiceError(... is ambiguous ...)` runs on quantities too. A string quantity such as `"1.250"` was read as 1.250 and is now refused. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ text = _plain_amount(value, label) if isinstance(value, str) else str(value).strip()` widens how an amount may be written; keys, date format and line count are still checked, and errors still name the field. |
| C2 | held | not touched; the gap is as it was (three capital letters only). |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched; `_cents(quantity * unit_price)` still computes the amount, `_plain_amount` only rewrites the operands the model reported. |
| C5 | held | not touched; `lines_total == total` still decides `status`, with no tolerance. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
