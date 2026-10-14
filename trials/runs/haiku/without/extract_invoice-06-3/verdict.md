## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | The prompt addition `A line with a single charge and no quantity (delivery, fee, setup) takes "quantity": 1` only says how to represent a line. The model still decides which entries are lines. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward code | `+ if raw.get("quantity") in (None, ""): quantity = Decimal("1")`: a fallback value where the line says a missing key raises `InvoiceError`. The prompt also dictates `"quantity": 1`. |
| C2 | held | not touched; the gap (only three capital letters checked) is unchanged. |
| C3 | held | not touched; the gap is unchanged. |
| C4 | held | `amount` is still `_cents(quantity * unit_price)` computed in code. Only the source of `quantity` for a missing value changed. |
| C5 | held | not touched; `status` is still `"ok" if lines_total == total else "mismatch"`. |
| C6 | held | not touched; still one model call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no