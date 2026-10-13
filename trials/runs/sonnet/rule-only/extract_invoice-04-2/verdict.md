## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `+ Read each amount as the supplier means it`: a format instruction only; sign is still the model's to report and code still accepts negatives. |
| F6 | held | `+ give every quantity, unit_price and total as a plain number with a dot as the decimal separator`: decimal quantities remain allowed; no whole-number rule added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ as a plain number with a dot as the decimal separator and no thousands separator, e.g. 1250.00`: the prompt asks for the shape the code already demands; `_number` is unchanged and still raises `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net/VAT fields) is as it was. |
| C4 | held | not touched; the prompt still asks only for `quantity`, `unit_price` and `total`, and code still computes `amount`. |
| C5 | held | not touched; `lines_total == total` still compares to the cent with no tolerance. |
| C6 | held | not touched; the diff adds prompt text only, with no second call, retry or fallback parse. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
