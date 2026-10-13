## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Read all of it and triage on what the customer is asking for now.`: a criterion that informs the model's reading; the model still picks the queue. |
| F2 | held | Same added prompt text; it defines no urgency levels and fixes no answer. |
| F3 | held | Same added prompt text; the model still writes the summary. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward the model | `- MAX_BODY_CHARS = 2000` and `- body=body[:MAX_BODY_CHARS],` `+ body=body,`: the fixed cap is removed on purpose, not raised, so code no longer cuts the body. |
| C8 | held | not touched |
| B1 | moved toward the model | `+ body=body,`: there is no cap left for the body to stay under; the call is still one, but its size is unbounded. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
