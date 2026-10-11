## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ "vat" (the tax amount, 0 if the invoice shows no tax)`: tax gets its own key, as C3 asks; the model still decides which entries are lines. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ vat = _cents(_number(raw_vat, "vat")) if raw_vat is not None else Decimal("0.00")`: a named key the prompt asks for can be absent or `null` without raising `InvoiceError`. |
| C2 | held | not touched; the gap is as it was. |
| C3 | moved toward the charter | `+ "vat": vat,` and `+ "status": "ok" if lines_total + vat == total else "mismatch"`: VAT is its own field and code checks net + VAT against the total. |
| C4 | held | not touched |
| C5 | held | `+ "status": "ok" if lines_total + vat == total else "mismatch"`: still exact to the cent with no tolerance, and the sum is done by code. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
