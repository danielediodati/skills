## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price" of the net amounts), "vat" (the tax amount shown`: a criterion, and the tax leaves the lines as C3 requires. The model still picks which entries are lines. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ vat = Decimal("0.00") if raw_vat is None else _cents(_number(raw_vat, "vat"))`: an answer missing the named key `vat` passes with a default instead of raising `InvoiceError`. |
| C2 | held | not touched; the gap is as it was. |
| C3 | moved toward the charter | `+ "vat": vat,` and `+ "status": "ok" if lines_total + vat == total else "mismatch",`: VAT is its own field, with the net + VAT = total arithmetic checked by code. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + vat == total else "mismatch",`: still exact to the cent, no tolerance; the added VAT term is the one C3 calls for. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: yes
- stopped: no
