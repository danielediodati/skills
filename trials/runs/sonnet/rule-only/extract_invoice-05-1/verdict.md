## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price" before any tax), "tax" (the total VAT or sales tax`: adds a field and a criterion for reading it; the model still decides which entries are lines. |
| F5 | held | `+ tax = Decimal("0") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: no sign rule added, negative amounts still pass. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: a named key missing or null is defaulted on purpose instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch",`: VAT becomes a separate field and code checks the arithmetic between lines, tax and total. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch",`: still an exact comparison to the cent with no tolerance; adding tax is the arithmetic C3 calls for. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call with no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
