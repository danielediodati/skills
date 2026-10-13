## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"quantity" and "unit_price"), "tax" (the VAT or tax amount charged on the`: tax is asked for as its own field, and the model still decides which entries are lines. |
| F5 | held | not touched; `_number(raw_tax, "tax")` accepts negative values as it does for the other amounts. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: a named key missing from the answer is accepted as 0 instead of raising `InvoiceError`, on purpose (`test_tax_is_not_waved_through_when_missing`). |
| C2 | held | not touched; the gap (three capital letters only) is left as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: VAT is a separate field and code checks the arithmetic between net, VAT and total. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `+ "status": "ok" if lines_total + tax == total else "mismatch"`: still an exact comparison to the cent in code, with no tolerance, now including the VAT that C3 calls for. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: yes
- stopped: no
