## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Base all three answers on what the customer is asking for now, not on how the message begins.`: a criterion that informs the reading; the model still picks the queue. |
| F2 | held | Same added prompt paragraph: criteria in the prompt, as the line allows; no level is defined or fixed by code. |
| F3 | held | `+ The customer's actual request can be anywhere in the message.`: guides what to read; the model still writes the summary. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general` and `normal` defaults remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- MAX_BODY_CHARS = 2000` `+ MAX_BODY_CHARS = 12000`: the cap is a budget number that may be raised; still one call, one fixed cut, no chunking or retry. |
| C8 | held | not touched |
| B1 | held | `+ MAX_BODY_CHARS = 12000`: still one model call per ticket, body up to the cap. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial