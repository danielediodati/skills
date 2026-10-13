## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ A charge printed as a single amount ... has "quantity" 1 and that amount as "unit_price".`: a general rule on how to report a line; the model still decides which entries are lines. |
| F5 | held | not touched; the new branch still passes the price through `_number`, which accepts negative amounts. |
| F6 | held | not touched; `+ quantity = Decimal("1")` applies only when no quantity is given and adds no whole-number rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ if raw.get("quantity") is None and (raw.get("unit_price") is not None or raw.get("amount") is not None):` a line missing the named key `quantity`, or carrying an unnamed `amount` key, no longer raises `InvoiceError`. |
| C2 | held | not touched; the gap is as it was. |
| C3 | held | not touched; the gap is as it was. |
| C4 | moved toward the model | `+ price = raw.get("amount")` with `+ quantity = Decimal("1")`: the line amount is now the model's own `amount` figure, not a product of a quantity and unit price it reported. |
| C5 | held | not touched; `"ok" if lines_total == total else "mismatch"` is unchanged. |
| C6 | held | not touched; still one `model(...)` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: yes
- stopped: no