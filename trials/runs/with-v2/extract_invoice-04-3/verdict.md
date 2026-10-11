## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `+ Report every quantity, unit_price and the total as a plain JSON number or a string of digits with a dot as the only decimal separator`: fixes how a number is written, not its sign; code still accepts negatives. |
| F6 | held | `+ with a dot as the only decimal separator and no thousands separator`: a notation rule the model applies by reading each invoice; non-integer quantities are still accepted. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ whatever the invoice uses` only tells the model how to write numbers; `_number` is unchanged and `+ extract(total="1.250,00")` still raises `total is not a number`. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT fields) is left as it was. |
| C4 | held | not touched: the prompt still asks only for `quantity` and `unit_price`, and code still computes each `amount`. |
| C5 | held | not touched: the comparison `lines_total == total` is unchanged, with no tolerance added. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call; no retry and no code fallback for locale-formatted amounts. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no
