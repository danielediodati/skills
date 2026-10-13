## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Judge the ticket on what the customer is asking for now, not on how the message begins.`: a criterion that informs the reading; the model still picks the queue. |
| F2 | held | The same added prompt text fixes no urgency level; no code touches the urgency. |
| F3 | held | `+ The customer's actual request can be anywhere in the message`: it tells the model where to look, not what the summary says. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults stay as they were, so the gap is neither closed nor widened. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- MAX_BODY_CHARS = 2000` / `+ MAX_BODY_CHARS = 12000`: the cap is a budget number the line says may be raised; still one call, a fixed cut, no chunking, no retry. |
| C8 | held | not touched |
| B1 | held | `+ MAX_BODY_CHARS = 12000`: still one model call per ticket, body up to the cap; only the budget number changed. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
