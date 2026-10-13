## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price"), "vat" (the VAT amount charged, 0 if the invoice`: VAT gets its own key, as C3 asks; the model still chooses which entries are lines. |
| F5 | held | `+ vat = _cents(_number(data.get("vat"), "vat"))`: `_number` accepts negatives, so credit notes still pass; the line handling is not touched. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ vat = _cents(_number(data.get("vat"), "vat"))`: the new key is required, and a missing or malformed one raises `InvoiceError` naming `vat`. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | moved toward the charter | `+ "vat": vat,` and `+ "status": "ok" if lines_total + vat == total else "mismatch"`: net, VAT and total are now separate fields, with the sum checked by code. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged, and the prompt asks for the VAT amount charged, not a computed one. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` / `+ "status": "ok" if lines_total + vat == total else "mismatch"`: still exact to the cent with no tolerance, and VAT enters as C3 requires. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, with no retry and no fallback. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: yes
- stopped: no
