## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ ...no thousands separators or currency symbols...` applies only to the amount fields; the model still infers the `currency` key by reading. |
| F4 | held | not touched |
| F5 | held | `+ Write every quantity, unit_price and total as a plain number` fixes notation only; a negative amount is still a plain number and still accepted by `_number`. |
| F6 | held | `+ ...with a dot as the decimal separator` keeps fractional quantities; no whole-number rule added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ Write every quantity, unit_price and total as a plain number with a dot as the decimal separator` tells the model the format code already demands; `_number` is unchanged and still raises `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (three capital letters only) is as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net/VAT) is as it was. |
| C4 | held | not touched; `amount` is still `_cents(quantity * unit_price)`, and the prompt asks only for quantity, unit_price and total. |
| C5 | held | not touched; `"ok" if lines_total == total else "mismatch"` unchanged, no tolerance added. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))`, no retry or fallback added (a retry is only named as an option left to the requester). |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
