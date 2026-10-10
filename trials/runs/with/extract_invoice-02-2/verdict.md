## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+The lines are the net items, without the tax.`: defines the new field's boundary as C3 asks; the model still decides which entries (delivery, discounts) are lines. |
| F5 | held | not touched; `_cents(_number(raw_tax, "tax"))` accepts negative tax as well. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: the prompt names a `"tax"` key, but its absence passes as 0 instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap is as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: tax is its own field and code checks the arithmetic; net is still only the computed `lines_total`. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch"`: still exact to the cent, no tolerance, with the tax term C3 calls for. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
