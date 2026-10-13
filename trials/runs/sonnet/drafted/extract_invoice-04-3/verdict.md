## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ no currency symbol (e.g. 1250.00)` only governs how amounts are written; which currency the invoice is in is still the model's reading. |
| F4 | held | not touched |
| F5 | held | `+ Write every quantity, unit_price and total as a plain number` sets notation only; no sign rule is added and `_number` still accepts negatives. |
| F6 | held | `+ digits with a full stop as the decimal separator` keeps decimal quantities; no whole-number rule is added in prompt or code. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ Write every quantity, unit_price and total as a plain number` is a general format rule; the code's shape checks are unchanged, and the new test confirms `"1.250,00"` still raises `total is not a number`. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net/VAT fields) is left as it was. |
| C4 | held | not touched; amounts are still `_cents(quantity * unit_price)`, and the model is asked to transcribe figures, not compute them. |
| C5 | held | not touched; `lines_total == total` still decides `ok` or `mismatch`, with no tolerance. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, and no retry or fallback parser was added for national number styles. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no