## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward code | `+ vat = _cents(_number(data.get("vat", 0), "vat"))`: a new named key gets a code default of 0 when absent, where the line raises `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | moved toward the charter | `+ "vat": vat`, `+ lines_total + vat == total`: VAT is now a separate field and the arithmetic between net, VAT and total is checked by code. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `- "ok" if lines_total == total` / `+ "ok" if lines_total + vat == total else "mismatch"`: still an exact-to-the-cent comparison in code, no tolerance. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call, no retry or fallback. |
| C7 | held | not touched. |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no