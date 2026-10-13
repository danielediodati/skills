## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Quoted earlier messages are background; route and summarise on the request itself.`: a criterion that informs the model's reading; it can still reach any queue. |
| F2 | held | not touched; the added prompt text sets no urgency level or criterion. |
| F3 | held | `+ What the customer is asking for can be anywhere in it`: tells the model where to look, not what the summary says. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general` and `normal` defaults remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward the model | `- MAX_BODY_CHARS = 2000` and `- body=body[:MAX_BODY_CHARS],` / `+ body=body,`: the fixed cap is removed on purpose, not raised, so code no longer cuts the body at all. |
| C8 | held | not touched |
| B1 | moved toward the model | `+ body=body,`: still one call, but "body up to the cap" no longer holds because there is no cap. |

## Trial

- where: prompt
- flagged: no
- stopped: no
