## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price" as printed, before tax), "tax" (the total VAT or`: tax gets its own key as C3 requires; the model still chooses which entries are lines. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: a missing or null `tax` key passes as zero instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (three capital letters only) is as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch",`: tax is its own field and code checks the arithmetic; net is still not a separate field. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged and tax is not a line amount. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch",`: still exact equality to the cent with no tolerance, with tax added as C3 asks. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
