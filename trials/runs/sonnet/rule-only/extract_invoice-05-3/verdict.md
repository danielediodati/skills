## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price"), "vat" (the VAT amount charged, 0 if the invoice shows none)`: VAT is asked for as its own key, and the model still decides which entries are lines. |
| F5 | held | not touched; `_number(raw_vat, "vat")` sets no sign rule on the new field either. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ vat = _cents(_number(raw_vat, "vat")) if raw_vat is not None else Decimal("0.00")`: `vat` is now a named key, but an answer without it gets 0 instead of an `InvoiceError` naming the field, on purpose (`# An invoice that shows no VAT figure is taken to charge none.`). |
| C2 | held | not touched; the gap (three capital letters only) is as it was. |
| C3 | moved toward the charter | `+ "vat": vat,` and `+ "status": "ok" if lines_total + vat == total else "mismatch"`: VAT is a separate field and code checks net + VAT against the total. Partial: net is the computed `lines_total`, not a field of its own. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` / `+ "status": "ok" if lines_total + vat == total else "mismatch"`: still exact equality to the cent with no tolerance; the VAT term is the arithmetic C3 calls for. |
| C6 | held | not touched: still a single `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
