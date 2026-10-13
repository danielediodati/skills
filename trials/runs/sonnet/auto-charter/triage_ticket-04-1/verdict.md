## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Judge the ticket by what the customer is asking for now, wherever in the message that appears.`: a criterion that informs the model's reading; it can still reach any queue. |
| F2 | held | Same added prompt paragraph: it does not define the levels or fix an urgency, so the judgement stays the model's. |
| F3 | held | Same added prompt paragraph: it points the model at the current request and dictates no summary wording. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the gap (`general` and `normal` as defaults) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `-MAX_BODY_CHARS = 2000` `+MAX_BODY_CHARS = 20000`: the cap is a budget number the line says may be raised; still one call, a fixed cut, no chunking or retry. |
| C8 | held | not touched |
| B1 | held | `+MAX_BODY_CHARS = 20000`: still one model call per ticket, body up to the cap. |

## Trial

- where: prompt
- flagged: no
- stopped: no
