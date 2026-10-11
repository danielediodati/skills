## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price"), "net" (the amount before VAT), "vat" (the VAT`: adds fields beside the lines; the model still decides which entries are lines. |
| F5 | held | `+ net = _cents(_number(data.get("net"), "net"))`: `_number` puts no sign rule on the new fields; negative amounts still pass. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ vat = _cents(_number(data.get("vat"), "vat"))`: the new keys are required and a missing or malformed one raises `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ consistent = lines_total == net and net + vat == total`: net, VAT and total are now separate fields and code checks the arithmetic between them. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if consistent else "mismatch"`: exact equality to the cent, no tolerance, now through net and VAT as C3 requires; otherwise `mismatch`. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, with no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
