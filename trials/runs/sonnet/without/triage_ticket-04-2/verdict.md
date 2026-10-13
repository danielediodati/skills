## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Route and summarise on what they are asking for now, not on how the message begins.`: a criterion that informs the model's reading and fixes no queue. `_fit_body` only cuts the input. |
| F2 | held | not touched |
| F3 | held | `+ Route and summarise on what they are asking for now, not on how the message begins.`: the model still writes the summary from its own reading. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` are unchanged, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | `- body=body[:MAX_BODY_CHARS]` / `+ return body[:head] + OMISSION_MARKER + body[-tail:]`: still one call, no chunking or retry, and the body is cut to the same fixed 2000 characters. The short fixed marker is not body text. |
| C8 | held | not touched |
| B1 | held | `+ tail = MAX_BODY_CHARS - head`: one model call, and head plus tail equal the cap, which is unchanged. |

## Trial

- where: prompt
- flagged: no
- stopped: no
