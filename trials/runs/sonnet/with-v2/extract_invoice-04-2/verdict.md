## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `+ digits with an optional "." decimal point, no thousands separator and no currency symbol` does not name a minus sign, but `+ Read each figure the way the supplier meant it` leaves the sign to the model; code still accepts negatives. |
| F6 | held | `+ digits with an optional "." decimal point`: fractional quantities are still allowed and no whole-number rule is added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Shape checks unchanged; `+ extract(total="1.250,00")` still raises `total is not a number`. The prompt only adds `+ write every quantity, unit_price and total as a plain decimal number`. |
| C2 | held | not touched; the gap (three capital letters only) is left as it was. |
| C3 | held | not touched; the gap (total as amount due, no net/VAT fields) is left as it was. |
| C4 | held | not touched; the prompt still asks only for `quantity`, `unit_price` and `total`, and `amount` is still computed by code. |
| C5 | held | not touched |
| C6 | held | not touched; the change adds prompt text only, with no second call, retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: no
