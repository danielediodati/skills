## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ "vat" (the tax amount, 0 if the invoice shows no tax)`: tax gets its own key as C3 requires; which entries are lines is still the model's reading. |
| F5 | held | `+ vat = _cents(_number(raw_vat, "vat"))`: no sign rule added; negative amounts still pass. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ ... if raw_vat is not None else Decimal("0.00")`: a named key the prompt asks for may be missing without `InvoiceError`. An answer that omits `vat` passes unchecked as tax-free. |
| C2 | held | not touched; the gap (three capital letters only) is as it was. |
| C3 | moved toward the charter | `+ "vat": vat,` and `+ "status": "ok" if lines_total + vat == total else "mismatch"`: VAT is its own field and code checks lines plus VAT against the total. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + vat == total else "mismatch"`: still exact to the cent with no tolerance. The VAT term is the one C3 calls for. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, with no retry or second call. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
