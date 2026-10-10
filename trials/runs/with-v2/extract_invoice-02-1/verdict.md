## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+The lines are the invoice's entries before tax.`: a criterion that keeps tax out of the lines, as C3 requires. The model still decides which entries (delivery, discounts) are lines. |
| F5 | held | not touched; `_cents(_number(raw_tax, "tax"))` accepts a negative tax, so credit notes still pass. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: the prompt names a `tax` key, but an answer missing it (or with null) passes with a default instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: tax is its own field and code checks the arithmetic. Closed in part: net is still `lines_total`, not a separate field read and checked. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` becomes `+ ... lines_total + tax == total ...`: still exact equality to the cent with no tolerance, in the form C3 asks for. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
