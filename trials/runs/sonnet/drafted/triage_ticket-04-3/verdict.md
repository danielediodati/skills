## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Base your answer on what they are asking for now, not on how the message begins.`: a criterion that informs the reading; the model still picks the queue. |
| F2 | held | Same added prompt paragraph: it defines no levels and fixes no urgency; the judgement stays the model's. |
| F3 | held | Same added prompt paragraph: it points the model at the current request but does not dictate what the summary says. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `-MAX_BODY_CHARS = 2000` / `+MAX_BODY_CHARS = 12000`: the cap is a budget number the line says may be raised; still one call, one fixed cut, no chunking or retry. |
| C8 | held | not touched |
| B1 | held | `+MAX_BODY_CHARS = 12000`: still one model call per ticket, with the body up to the (raised) cap. |

## Trial

- where: both
- flagged: yes
- stopped: no