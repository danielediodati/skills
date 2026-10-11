## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Route on what the customer is asking for, wherever in the message it appears.` and `+Do not route on the quoted or older topic if the customer is now asking about something else.`: criteria that inform the reading; the model still picks the queue. |
| F2 | held | not touched: the added prompt text speaks of routing only, and the urgency levels stay undefined in the prompt and in code. |
| F3 | held | not touched: `summary: one sentence saying what the customer needs` is unchanged, and no code writes or overrides the summary. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched: the tier is still absent from the prompt, and the enterprise raise is unchanged. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- body=body[:MAX_BODY_CHARS],` `+ body=_shorten(body),` with `+ return body[:BODY_HEAD_CHARS] + OMISSION_MARK + body[-BODY_TAIL_CHARS:]`: still one call, and the body is still cut by code to the fixed 2000 characters (600 + 1400). There is no chunking across calls, no retry and no merge. |
| C8 | held | not touched |
| B1 | held | `+BODY_TAIL_CHARS = MAX_BODY_CHARS - BODY_HEAD_CHARS`: one call, and the body text kept stays at the 2000 cap. Only a fixed omission marker is added, which is not ticket body. |

## Trial

- where: prompt
- flagged: no
- stopped: no
