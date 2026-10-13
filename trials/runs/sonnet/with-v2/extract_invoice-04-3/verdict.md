## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `+ Report every quantity, unit_price and the total as a plain JSON number or a string of digits with a dot as the only decimal separator`: fixes notation only; `_number` still accepts negatives. |
| F6 | held | `+ with a dot as the only decimal separator and no thousands separator`: decimals are still allowed, with no whole-number rule in prompt or code. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ Report every quantity, unit_price and the total as a plain JSON number or a string of digits with a dot...`: the prompt asks for the shape code already requires; `_number` is unchanged and still raises `InvoiceError` on `1.250,00`. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT fields) is left as it was. |
| C4 | held | `+ Report every quantity, unit_price and the total...`: the model still reports only quantity and unit price; code still computes `amount`. |
| C5 | held | not touched |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, with no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no
