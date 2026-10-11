## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `+ write every quantity, unit_price and total as a plain decimal number: digits with an optional "." decimal point` fixes notation only; the model still reports negative amounts and code still accepts them. |
| F6 | held | `+ digits with an optional "." decimal point`: non-integer quantities are still allowed and no whole-number rule is added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ no thousands separator and no currency symbol (1250.00)` asks for the shape code already requires; `_number` still raises `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT fields) is as it was. |
| C4 | held | not touched; `amount` is still `_cents(quantity * unit_price)` in code, and the prompt asks only for quantity, unit_price and total. |
| C5 | held | not touched; `lines_total == total` still decides `ok` or `mismatch`, with no tolerance. |
| C6 | held | not touched; the change adds prompt text only, with no second call, retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no
