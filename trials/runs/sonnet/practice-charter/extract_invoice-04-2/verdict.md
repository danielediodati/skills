## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `+Write every number as a plain decimal with a point as the decimal separator`: a format rule only; the sign is not restricted and the model still reports negative amounts. |
| F6 | held | `+Write every number as a plain decimal`: decimals are explicitly allowed, so there is no whole-number rule on quantities. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+no thousands separators or currency symbols, whatever the invoice's own convention`: a general format rule the model applies by reading; the shape checks and `InvoiceError` in code are unchanged. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT fields) is left as it was. |
| C4 | held | not touched; `_cents(quantity * unit_price)` still computes each line amount in code. |
| C5 | held | not touched; `lines_total == total` is still compared exactly, with no tolerance. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, with no retry or fallback added. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
