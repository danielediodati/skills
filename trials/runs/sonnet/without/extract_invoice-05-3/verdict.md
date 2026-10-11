## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ "tax" (the total VAT or other tax charged, or 0 if none)` adds a field beside the lines; the model still decides which entries are lines. |
| F5 | held | not touched; the new `tax` and `subtotal` pass through `_number`, which accepts negatives. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Checks on the existing keys not touched; `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))` still raises on a malformed value. A missing tax becomes 0 and still faces the sum check. |
| C2 | held | not touched; the gap is as it was. |
| C3 | moved toward the charter | `+ consistent = lines_total + tax == total and subtotal in (None, lines_total)`: subtotal, tax and total are now separate fields with the arithmetic checked by code. Closed in part: subtotal may be `null`. |
| C4 | held | not touched |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` becomes `lines_total + tax == total`: still exact to the cent, no tolerance, otherwise `mismatch`. The tax term is the one C3 calls for. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
