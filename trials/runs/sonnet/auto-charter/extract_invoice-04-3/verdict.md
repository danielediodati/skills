## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched: `+Write every number as a plain decimal with a period as the decimal separator` fixes notation only, and the sign is still the model's reading. |
| F6 | held | not touched: `+Write every number as a plain decimal` still allows fractional quantities. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+Write every number as a plain decimal with a period as the decimal separator` asks the model for the shape the code already demands; `_number` and its `InvoiceError` are unchanged. |
| C2 | held | not touched: the gap (only three capital letters checked) is as it was. |
| C3 | held | not touched: the gap (total is the amount due, no net or VAT fields) is as it was. |
| C4 | held | not touched: the amount is still `_cents(quantity * unit_price)`; the prompt line `+and no thousands separators, whatever notation the invoice uses` asks the model to transcribe figures, not compute amounts. |
| C5 | held | not touched: `lines_total == total` is unchanged, with no tolerance added. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, with no retry or fallback added. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no
