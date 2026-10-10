## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price" of the net amounts), "vat" (the tax amount shown`: tells the model where tax goes, as C3 requires; which entries are lines is still its reading. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ vat = Decimal("0.00") if raw_vat is None else _cents(_number(raw_vat, "vat"))`: an answer missing the named key `vat` passes as zero instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | moved toward the charter | `+ "vat": vat,` and `+ "status": "ok" if lines_total + vat == total else "mismatch",`: VAT is its own field and code checks the arithmetic; closes the gap in part (net is still only `lines_total`). |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged, and `vat` is not a line amount. |
| C5 | held | `+ "status": "ok" if lines_total + vat == total else "mismatch",`: still exact to the cent with no tolerance, otherwise `mismatch`; the added term is the VAT arithmetic C3 asks for. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: yes
- stopped: no
