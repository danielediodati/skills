## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | `+ Decide which from the evidence in the invoice: the supplier's country, the currency, the language, the layout...`: criteria that inform the model's reading without fixing its answer; no day-month rule in code. |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | not touched; `issue_date` is still required as `YYYY-MM-DD` and parsed by `date.fromisoformat`, with no new key or status added. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total as amount due, no net/VAT fields) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched; the added prompt text sits in the same single call, with no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial