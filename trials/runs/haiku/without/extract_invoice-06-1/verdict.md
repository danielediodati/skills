## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | The added prompt sentence `A single charge with no quantity printed, such as a delivery or a fee, has quantity 1` is about quantity, not about which entries are lines; the model still decides what counts as a line. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward code | `+ quantity_value = 1 if raw.get("quantity") is None else raw.get("quantity")`: a default replaces the `InvoiceError` naming the field, so a missing key no longer raises. |
| C2 | held | not touched; the gap ("Not yet in code") is unchanged. |
| C3 | held | not touched; the gap ("Not yet in code") is unchanged. |
| C4 | held | Amounts are still `_cents(quantity * unit_price)` computed by code; the default only supplies `quantity`, and the model's amount is still not read. |
| C5 | held | The comparison `lines_total == total` is untouched, so `mismatch` is still produced with no tolerance. |
| C6 | held | not touched; still one call to `model`, no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no