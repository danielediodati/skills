## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price" - the net price, before tax), "tax" (the total tax amount, VAT or similar; 0 if the invoice shows none)`: tax gets its own field, as C3 asks; the model still picks which entries are lines. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ if data.get("tax") is None:` / `+ tax = Decimal("0.00")`: a named key missing from the answer passes with a default instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch",`: tax is a separate field and code checks the arithmetic; net is still only `lines_total`. |
| C4 | held | not touched; line amounts are still `_cents(quantity * unit_price)`. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch",` / `+ "status": "ok" if lines_total + tax == total else "mismatch",`: still exact equality to the cent, no tolerance, otherwise `mismatch`. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
