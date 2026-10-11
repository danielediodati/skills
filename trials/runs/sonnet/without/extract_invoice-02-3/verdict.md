## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price" as printed, before tax), "tax" (the total VAT or tax amount, 0 if the invoice shows none)`: defines the tax field C3 calls for; the model still reads which entries are lines. |
| F5 | held | not touched; `_number(raw_tax, "tax")` accepts negative tax as it does any amount. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: a named key that is missing or `null` passes with a default instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (three capital letters only) is as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: VAT is its own field and code checks the arithmetic; closes the gap in part (net is still only `lines_total`). |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `- "status": "ok" if lines_total == total` / `+ "status": "ok" if lines_total + tax == total`: still exact equality to the cent, no tolerance, otherwise `mismatch`. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
