## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `+ match = re.fullmatch(r"([+-]?)(\d[\d.,]*)", compact)` and `return sign + ...`: the sign is carried through, so negative amounts are still accepted as the model reports them. |
| F6 | moved toward code | `+ if len(tail) == 3 and head != "0" and head != "":` / `+ raise InvoiceError(f"{error} (ambiguous separator)")` runs on quantities too: a quantity the model writes as `"1.250"` or `"2,375"` is now refused by a code rule where it loaded before. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Keys, date format and the line check are not touched; `_plain_number` still raises `InvoiceError(error)` with the field's label for amounts it cannot read. |
| C2 | held | not touched; the gap to ISO 4217 is as it was. |
| C3 | held | not touched; the gap on net, VAT and total is as it was. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged, only the parsing of its operands in `_number` changed. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))`, no retry or fallback added. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: code
- flagged: no
- stopped: no
