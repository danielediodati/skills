## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ "vat" (the total VAT amount, or null if the invoice shows none)` asks for the VAT figure but does not tell the model which entries are lines; that reading stays with the model. |
| F5 | held | not touched; the new `vat` and `subtotal` go through the same `_number`, which accepts negatives. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Checks on the existing keys are untouched; `+ vat = _cents(_number(data.get("vat"), "vat")) if _given(data.get("vat")) else Decimal("0.00")` still raises `InvoiceError` naming the field when malformed. Null is the value the prompt defines for an invoice showing no VAT. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ consistent = lines_total + vat == total and subtotal in (None, lines_total)` and `+ "vat": vat,`: VAT is now a separate field and code checks the arithmetic between net, VAT and total. The gap closes in part: the stated subtotal is checked but not returned. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged and no amount is read from the model. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` becomes `+ "status": "ok" if consistent else "mismatch"`: still exact to the cent, no tolerance, otherwise `mismatch`. The added VAT term is the arithmetic C3 calls for. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))`, no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
