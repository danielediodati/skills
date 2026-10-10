## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price" -- net of tax), "tax" (the total tax, e.g. VAT,`: tax gets its own field as C3 asks; the model still decides which entries are lines. |
| F5 | held | not touched; the new `tax` goes through `_number`, which accepts negative amounts. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: a missing or null `tax` key passes as 0.00 instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch",`: tax is a separate field and code checks net + tax against the total. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch",`: still exact equality to the cent with no tolerance, with the tax term C3 calls for. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call with no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
