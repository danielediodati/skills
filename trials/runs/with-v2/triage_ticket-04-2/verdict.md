## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Read the whole message and triage what the customer is asking for now, not` / `+ what the thread started as or what the message opens with.`: a criterion that informs the reading; the model still picks the queue. |
| F2 | held | Same added prompt paragraph: it does not define the levels or fix an urgency; the judgement stays the model's. |
| F3 | held | `+ The customer's actual request can be anywhere in the message, often at the` `+ end`: tells the model where to look, not what the summary says. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the "Not yet in code" gap is left as it was. |
| C4 | held | not touched: the tier is still absent from the prompt and code still raises `enterprise` one level. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `-MAX_BODY_CHARS = 2000` `+MAX_BODY_CHARS = 20000`: the cap is a budget number the line says may be raised; still one call, a fixed cut, no chunking, no retry. |
| C8 | held | not touched |
| B1 | held | `+MAX_BODY_CHARS = 20000`: still one model call per ticket, body up to the cap; only the budget number changed. |

## Trial

- where: prompt
- flagged: no
- stopped: no
