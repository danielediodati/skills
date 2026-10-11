## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ "tax" (the total tax amount, VAT or similar; 0 if the invoice shows none)`: tax gets its own field as C3 requires; the model still decides which entries are lines. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ if data.get("tax") is None: tax = Decimal("0.00")`: a named key the model omits passes with a default instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: tax is a separate field and code checks the arithmetic; closes the gap in part. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch"`: still exact to the cent with no tolerance; the tax term is the one C3 calls for. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
