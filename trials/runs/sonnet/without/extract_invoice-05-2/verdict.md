## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | The prompt adds `"vat" (the total VAT amount, or null if the invoice shows none)` but does not tell the model which entries are lines; that is still its reading. |
| F5 | held | not touched; the new `vat` and `subtotal` go through `_number`, which accepts negative values. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Existing keys are checked as before; the new `vat` and `subtotal` are nullable by the prompt and, when given, pass through `_number(data.get("vat"), "vat")`, which raises `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (three capital letters only) is as it was. |
| C3 | moved toward the charter | `+ "vat": vat,` and `+ consistent = lines_total + vat == total and subtotal in (None, lines_total)`: VAT is a separate field and code checks net + VAT = total. Partial: the stated subtotal is not returned. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged, and `subtotal` is only compared with the lines, never used in their place. |
| C5 | held | `+ "status": "ok" if consistent else "mismatch"` with `lines_total + vat == total`: still exact to the cent with no tolerance, and with no VAT it is the old comparison. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call, with no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
