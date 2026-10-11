## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ elif first in "+" or first.isspace() or first.isalpha() or unicodedata.category(first) == "Sc":` peels symbols and codes off amounts only; the `currency` field is still the model's answer. |
| F4 | held | not touched |
| F5 | held | `+ if s.startswith("(") and s.endswith(")"):` and `+ negative = negative or signs == 1`: negative amounts are still accepted, in more written forms than before. |
| F6 | moved toward code | `+ if len(fraction) == 3 and 1 <= len(whole) <= 3 and whole != "0":` sits in `_number`, which also reads `quantity`. A quantity the model writes as `"1.250"` was read as 1.25 and is now refused by a code rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ number = _parse_amount(value, label)`: code still reads each amount deterministically, and what it cannot read still raises `InvoiceError` naming the field. |
| C2 | held | not touched; the gap is as it was. |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched: `_cents(quantity * unit_price)` is unchanged, only the reading of its operands changed. |
| C5 | held | not touched |
| C6 | held | not touched: no second call, and ambiguous amounts `raise fail` rather than fall back. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
