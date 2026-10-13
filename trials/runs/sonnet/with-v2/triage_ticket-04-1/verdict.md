## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Quoted text and logs are context, not the request.`: a criterion that informs the model's reading; it fixes no queue. |
| F2 | held | `+ Read the whole message before answering.`: no urgency level is defined or dictated; the judgement stays the model's. |
| F3 | held | `+ The customer's actual request can be anywhere in it`: guides what the model reads; the model still writes the summary. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- MAX_BODY_CHARS = 2000` `+ MAX_BODY_CHARS = 12000`: the cap is a budget number and may be raised; still one call, a fixed cut, no chunking or retry. |
| C8 | held | not touched |
| B1 | held | `+ MAX_BODY_CHARS = 12000`: still one model call per ticket, with the body up to the (raised) cap. |

## Trial

- where: prompt
- flagged: no
- stopped: no
