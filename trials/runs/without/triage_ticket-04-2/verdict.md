## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Route and summarise on what they are asking for now, not on how the message begins.`: a criterion that informs the reading; the model still picks the queue. |
| F2 | held | not touched |
| F3 | held | `+ Route and summarise on what they are asking for now, not on how the message begins.`: a criterion; the model still writes the summary. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general` and `normal` defaults remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- body=body[:MAX_BODY_CHARS]` / `+ return body[:head] + OMISSION_MARKER + body[-tail:]`: still one call, body still cut to the same 2000-character cap by code; no chunking, retry or merge. |
| C8 | held | not touched |
| B1 | held | `+ tail = MAX_BODY_CHARS - head`: one call, and head plus tail equal the cap; only the fixed marker is added. |

## Trial

- where: prompt
- flagged: no
- stopped: no
