## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price"), "tax" (the VAT or other tax amount charged on`: asks for the tax amount but does not say which entries are or are not lines; the model still decides. |
| F5 | held | not touched; `_cents(_number(raw_tax, "tax"))` accepts a negative tax as well. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: a named key the model omits or returns as null passes with a default instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: tax is its own field and code checks the arithmetic with the total; closes the gap in part. |
| C4 | held | not touched; line amounts are still `_cents(quantity * unit_price)`. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch"`: still exact to the cent with no tolerance, otherwise `mismatch`; the tax term is the one C3 calls for. |
| C6 | held | not touched; still one `model(...)` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
