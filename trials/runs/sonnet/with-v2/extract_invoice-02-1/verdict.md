## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+The lines are the invoice's entries before tax.`: a general definition the model still applies by reading each invoice; delivery and discounts stay its call, and it keeps tax out of the lines as C3 asks. |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: the prompt names `"tax"` as a key, but an answer that omits it passes with a default instead of raising `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | moved toward the charter | `+ "tax": tax,` and `+ "status": "ok" if lines_total + tax == total else "mismatch"`: tax is its own field beside `lines_total` and `total`, and code checks the arithmetic between them. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged, and tax is not a line amount. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` / `+ "status": "ok" if lines_total + tax == total else "mismatch"`: still exact equality to the cent with no tolerance; the added term is the one C3 calls for. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, with no retry. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
