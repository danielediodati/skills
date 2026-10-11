## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ "net" (the amount before VAT), "vat" (the VAT amount, 0 if the invoice has none)`: adds fields to report; the model still decides which entries are lines. |
| F5 | held | not touched; `+ vat = _cents(_number(data.get("vat"), "vat"))` uses the same `_number`, which accepts negatives. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ net = _cents(_number(data.get("net"), "net"))` and the same for `vat`: the new keys are required and raise `InvoiceError` naming the field, as for the others. |
| C2 | held | not touched; the gap (three capital letters only) is left as it was. |
| C3 | moved toward the charter | `+ consistent = lines_total == net and net + vat == total` with `+ "net": net, "vat": vat,`: separate fields, with the arithmetic checked by code. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` / `+ "status": "ok" if consistent else "mismatch"`: still exact equality to the cent, now through net and VAT as C3 requires. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
