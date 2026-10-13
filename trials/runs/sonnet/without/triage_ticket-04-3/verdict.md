## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Route on what the customer is asking for, wherever in the message it appears.` / `+Do not route on the quoted or older topic if the customer is now asking about something else.`: a criterion that informs the model's reading; the model still picks the queue. |
| F2 | held | not touched |
| F3 | held | not touched: the added prompt text speaks of routing, and the model still writes the summary. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults stay as they were, so the gap is neither closed nor widened. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- body=body[:MAX_BODY_CHARS],` `+ body=_shorten(body),` with `return body[:BODY_HEAD_CHARS] + OMISSION_MARK + body[-BODY_TAIL_CHARS:]`: still one call, body still cut by code to the fixed 2000 characters (600 + 1400), no chunking, no retry. |
| C8 | held | not touched |
| B1 | held | `+BODY_TAIL_CHARS = MAX_BODY_CHARS - BODY_HEAD_CHARS`: one model call, and the body kept is still at most the cap, `MAX_BODY_CHARS` unchanged. |

## Trial

- where: prompt
- flagged: no
- stopped: no
