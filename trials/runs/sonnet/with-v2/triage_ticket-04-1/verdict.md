## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ The customer's actual request can be anywhere in it` and `+ Quoted text and logs are context, not the request.`: criteria that inform the reading; the model still picks the queue. |
| F2 | held | not touched: the added prompt text names no urgency level and sets no rule for one. |
| F3 | held | `+ Read the whole message before answering.`: a criterion for what to read; the model still writes the summary. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults remain, so the gap is as it was. |
| C4 | held | not touched: the prompt still receives only subject and body, and code still raises `enterprise` one level. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `-MAX_BODY_CHARS = 2000` / `+MAX_BODY_CHARS = 12000`: the cap is a budget number the line says may be raised; still one call, a fixed cut, no chunking, no retry. |
| C8 | held | not touched |
| B1 | held | `+MAX_BODY_CHARS = 12000`: still one model call per ticket, with the body up to the raised cap. |

## Trial

- where: prompt
- flagged: no
- stopped: no
