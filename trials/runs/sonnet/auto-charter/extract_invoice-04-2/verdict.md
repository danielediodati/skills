## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `+Write every number the way a program reads it: digits with "." as the decimal`: fixes notation only; sign and value are still the model's reading, and code adds no sign rule. |
| F6 | held | `+point and no thousands separators, whatever convention the invoice uses`: decimal quantities are still allowed; no whole-number rule is added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+Write every number the way a program reads it`: the prompt asks for a readable form, but `_number` and the other shape checks are unchanged and still raise `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net/VAT fields) is left as it was. |
| C4 | held | `+("1.250,00" is 1250.00, "1,250.00" is 1250.00).`: the model transcribes the printed quantity and unit price; `_cents(quantity * unit_price)` is unchanged and still computes the amount. |
| C5 | held | not touched; `"ok" if lines_total == total else "mismatch"` is unchanged, with no tolerance added. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, with no retry or fallback on an unreadable number. |
| C7 | held | not touched; number notation is not among the listed mechanical steps, and the three listed are unchanged. |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no
