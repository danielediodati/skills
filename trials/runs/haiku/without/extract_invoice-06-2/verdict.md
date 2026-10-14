## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | The prompt's `A charge printed as a single amount, such as a delivery, set-up or fee, has quantity 1 and unit_price equal to that amount.` is a rule the model applies by reading; it does not change which entries count as lines. |
| F5 | held | not touched |
| F6 | held | A quantity that is present is still read by `_number` and can be fractional; only the missing case changes. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward code | `+ if raw.get("quantity") in (None, ""): quantity = Decimal("1")`: a code default fills a missing line field where the line says anything else raises `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as before. |
| C3 | held | not touched; the gap is as before. |
| C4 | held | Amounts are still `_cents(quantity * unit_price)` computed in code; the model supplies no amount. |
| C5 | held | not touched; `"ok" if lines_total == total else "mismatch"` is unchanged. |
| C6 | held | not touched; still one `model(...)` call, no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: both
- flagged: yes
- stopped: no