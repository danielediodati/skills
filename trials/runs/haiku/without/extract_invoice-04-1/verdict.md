## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the currency handling is unchanged; the new parser only strips currency signs from amounts. |
| F4 | held | not touched |
| F5 | held | `sign = "-" if match.group(1).startswith("-") else ""` keeps the sign, so negative amounts still pass. |
| F6 | moved toward code | `elif dots + commas == 1 and not (len(body) - last - 1 == 3 and body[:last] != "0")`: code reads a lone separator before three digits as thousands. A quantity string `"2.500"` (2.5 kg) becomes 2500 without the model deciding. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | the keys, date format and at-least-one-line checks are not touched. Only the numeric parse was widened, and the line does not cover it. |
| C2 | held | not touched: still only the `[A-Z]{3}` check, so the gap is as it was. |
| C3 | held | not touched: still no net/VAT split, so the gap is as it was. |
| C4 | held | `"amount": _cents(quantity * unit_price)` is unchanged; code still computes the amounts. |
| C5 | held | `"status": "ok" if lines_total == total else "mismatch"` is unchanged, with no tolerance added. |
| C6 | held | not touched: still one `model(...)` call, no retry. |
| C7 | held | the empty-text refusal, fence-tolerant JSON read and `.upper()` are unchanged. |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: code
- flagged: no
- stopped: no