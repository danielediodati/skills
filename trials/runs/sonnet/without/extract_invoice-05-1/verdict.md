## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price"), "vat" (the VAT amount charged, 0 if the invoice`: asks for a VAT figure as its own key; the model still decides which entries are lines. |
| F5 | held | not touched; `_number(raw_vat, "vat")` puts no sign rule on the new amount either. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ vat = Decimal("0.00") if raw_vat is None else _cents(_number(raw_vat, "vat"))`: a key the prompt names may be absent or null and passes as 0 instead of raising `InvoiceError` naming the field; deliberate (`test_vat_missing_means_no_vat`). |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | moved toward the charter | `+ "vat": vat,` and `+ "status": "ok" if lines_total + vat == total else "mismatch",`: VAT is a separate field and code checks the arithmetic between lines, VAT and total; closes the gap in part. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + vat == total else "mismatch",`: still exact equality to the cent, no tolerance, otherwise `mismatch`; the VAT term is the one C3 calls for. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
