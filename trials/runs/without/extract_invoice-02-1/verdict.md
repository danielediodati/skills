## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price" -- net of tax), "tax" (the total tax, e.g. VAT,`: defines the fields; the model still reads each invoice to decide which entries are lines. |
| F5 | held | not touched; `_cents(_number(raw_tax, "tax"))` accepts negative amounts as before. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: a named key the prompt asks for can be missing or null without raising `InvoiceError`. |
| C2 | held | not touched; the gap is left as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch",`: tax is its own field and code checks the arithmetic; net is still only the lines total. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch",`: still exact to the cent with no tolerance; the tax term is the one C3 calls for. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
