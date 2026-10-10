## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ Lines are net of tax.` keeps the tax out of the lines, as C3 requires; the model still decides which entries (delivery, discounts) are lines. |
| F5 | held | `+ _cents(_number(raw_tax, "tax"))`: no sign rule added; negative amounts still pass. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: the prompt names a `"tax"` key, but an answer without it no longer raises `InvoiceError` and can come out `ok`. |
| C2 | held | not touched; the gap is as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: tax is its own field and code checks the arithmetic. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged, and no amount is read from the model. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch"`: still exact equality to the cent, no tolerance, otherwise `mismatch`. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
