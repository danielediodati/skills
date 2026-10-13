## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | `+ Urgency means how soon the customer is hurt, not how important the customer is:` and the four level definitions are criteria in the prompt, which the line allows. The model still reads each ticket: an invoice copy with a Friday deadline can still be `high` under `+ high: a real problem or a firm deadline within days`. |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | The added prompt text defines the same four levels, `urgent`, `high`, `normal`, `low`; the closed set and `_choice` are unchanged. |
| C3 | held | not touched; the gap (`general` and `normal` defaults) is left as it was. |
| C4 | held | not touched; `+ not how important the customer is` does not pass the tier to the model, and the one-level enterprise raise in code is unchanged. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched; still one call, and the body cap is unchanged. |
| C8 | held | not touched |
| B1 | held | not touched; one model call per ticket, body up to the cap. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial