## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+The lines are the net items, without the tax.`: a general rule that follows C3's separate VAT field; the model still reads each invoice to decide which entries are lines. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: the prompt names a `tax` key, but an answer without it gets a fallback value instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: VAT is now its own field and code checks net + VAT against the total. It closes the gap in part. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged and no line amount is read from the model. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` / `+ "status": "ok" if lines_total + tax == total else "mismatch"`: still exact equality to the cent, no tolerance, with the tax term C3 calls for. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, with no retry. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
