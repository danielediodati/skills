## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ A line printed as a single amount, with no quantity or unit price (a delivery charge or flat fee), has "quantity" and "unit_price" null`: says how to report such a line, and the model still decides which entries are lines. |
| F5 | held | not touched; a negative flat amount still passes through `_number`. |
| F6 | held | `+ quantity = Decimal("1")` applies only when the model reports no quantity; non-integer quantities are accepted as before. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ else: quantity = _number(raw.get("quantity"), f"line {number} quantity")`: a line with neither the pair nor an `amount`, or only one of the pair, still raises `InvoiceError` naming the field. Top-level keys, date and the one-line minimum are untouched. |
| C2 | held | not touched; the gap is left as it was (still only three capital letters). |
| C3 | held | not touched; the gap is left as it was (total is still the amount due, no net or VAT fields). |
| C4 | moved toward the model | `+ unit_price = _number(raw.get("amount"), f"line {number} amount")` with `+ the printed figure as "amount"`: a line amount is now read from the model. Any line the model returns with null `quantity` and `unit_price` skips the code's quantity × unit price. |
| C5 | held | not touched; `lines_total == total` still decides `ok` or `mismatch` with no tolerance. |
| C6 | held | not touched; still one `model(...)` call, no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no