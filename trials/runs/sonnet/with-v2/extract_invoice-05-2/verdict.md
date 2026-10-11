## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price"), "vat" (the VAT amount charged, 0 if the invoice shows none)`: VAT gets its own field as C3 requires; the model still decides which entries are lines. |
| F5 | held | `+ vat = _cents(_number(data.get("vat"), "vat"))`: no sign rule added; negative amounts still pass. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ vat = _cents(_number(data.get("vat"), "vat"))`: the new key is checked like the others and raises `InvoiceError` naming the field ("vat is missing"). |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ "vat": vat,` and `+ "status": "ok" if lines_total + vat == total else "mismatch"`: VAT is a separate field and code checks net + VAT against the total. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` / `+ "status": "ok" if lines_total + vat == total else "mismatch"`: still exact to the cent with no tolerance; the added term is the VAT that C3 calls for. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: yes
- stopped: no
