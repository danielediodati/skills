## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"tax" (the VAT or other tax amount charged on the invoice, 0 if there is none)`: asks for a tax amount but does not fix which entries are lines; the model still decides. |
| F5 | held | not touched; `_number(raw_tax, "tax")` accepts negative values as it does elsewhere. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: the prompt now names a `tax` key, but an answer that omits it or gives null passes as 0.00 instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: tax is its own field and code checks the arithmetic with the total. Closes the gap in part: net is the computed `lines_total`, not a separate field. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged; tax is not a line amount. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` / `+ "status": "ok" if lines_total + tax == total else "mismatch"`: still exact equality to the cent, no tolerance, otherwise `mismatch`; the added term is the VAT arithmetic C3 calls for. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
