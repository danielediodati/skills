## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: `+ ... no thousands separator or currency symbol` concerns how numbers are written, not which currency the model infers. |
| F4 | held | not touched |
| F5 | held | `+ Write every number ("quantity", "unit_price", "total") as plain digits with a point as the decimal separator` fixes notation only; `_number` still accepts negative values. |
| F6 | held | `+ ... with a point as the decimal separator` keeps fractional quantities; no whole-number rule added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Shape checks unchanged; `+ Write every number ... as plain digits` only tells the model how to meet the check, and `_number` still raises `InvoiceError` naming the field. |
| C2 | held | not touched: the gap stays as it was, code still only checks three capital letters. |
| C3 | held | not touched: the gap stays as it was, total is still the amount due. |
| C4 | held | not touched: `amount` is still `_cents(quantity * unit_price)`; the prompt asks the model to rewrite notation, not to compute. |
| C5 | held | not touched: `lines_total == total` still compared to the cent, no tolerance. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry or fallback added. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: prompt
- flagged: yes
- stopped: no