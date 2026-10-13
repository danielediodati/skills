## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+"subtotal" (the amount before VAT or other tax, or null if the invoice does not show one), "tax" (the total VAT or other tax charged, or 0 if none)`: the model still reads which entries are lines and which is tax; nothing is fixed by rule. |
| F5 | held | not touched; `_number` still accepts negative values, for the new fields too. |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `+ tax = Decimal("0.00") if raw_tax is None else _cents(_number(raw_tax, "tax"))`: the prompt names `tax` as a key, yet an answer without it passes as 0 instead of raising `InvoiceError` naming the field. Done on purpose ("A missing tax counts as 0"). |
| C2 | held | not touched; the gap (three capital letters only) is left as it was. |
| C3 | moved toward the charter | `+ consistent = lines_total + tax == total and subtotal in (None, lines_total)` with `subtotal` and `tax` returned as separate fields: net, VAT and total are now separate and code checks the arithmetic. Partial, since the net may be `null`. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | `- "status": "ok" if lines_total == total else "mismatch"` / `+ "status": "ok" if consistent else "mismatch"`: still exact equality to the cent with no tolerance; the tax term is the separation C3 calls for. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))`, no retry or fallback call. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
