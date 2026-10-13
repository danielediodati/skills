## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | The prompt's `"lines"` wording is unchanged; the model still decides which entries are lines, and VAT only gains its own field: `"vat" (the VAT amount, 0 if the invoice has none)`. |
| F5 | held | not touched; `+ net = _cents(_number(data.get("net"), "net"))` adds no sign rule. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ net = _cents(_number(data.get("net"), "net"))` and `+ vat = _cents(_number(data.get("vat"), "vat"))`: the new keys raise `InvoiceError` naming the field, like the others. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ consistent = lines_total == net and net + vat == total` with `"net"`, `"vat"` and `"total"` as separate fields: the arithmetic between them is now checked by code. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` becomes `+ "status": "ok" if consistent else "mismatch"`: still exact to the cent, no tolerance, now through net and VAT as C3 asks. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
