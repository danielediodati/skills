## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched; the new parser reads amounts only, dates still go through `date.fromisoformat`. |
| F3 | held | `+ re.sub(r"EUR\|GBP\|USD\|CHF\|€\|£\|\$", "", ...)` strips symbols from amounts only; the currency field is still read by the model. |
| F4 | held | not touched |
| F5 | held | `+ re.fullmatch(r"(-?)(\d+(?:[.,]\d+)*)", s)` keeps the sign, so negative amounts such as `-12,5` still pass. |
| F6 | moved toward code | `+ if len(frac) == 3 and int_part != "0": raise InvoiceError(...could be read two ways...)`: `_number` also reads quantities, so a string quantity like `"2.500"` (metres) that parsed before is now refused by code. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Still one JSON object, named keys, ISO date, at least one line; the added `_plain_decimal` only normalizes amount strings and errors still name the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | held | not touched; the gap (no net/VAT/total fields) is as it was. |
| C4 | held | `"amount": _cents(quantity * unit_price)` is unchanged and still computed by code. |
| C5 | held | `"ok" if lines_total == total else "mismatch"` is unchanged, with no tolerance. |
| C6 | held | not touched; still one `model(...)` call and no retry. |
| C7 | held | Empty-text refusal, JSON extraction from fences and `.upper()` are unchanged. |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: code
- flagged: no
- stopped: no