## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model's valid queue is used as given. |
| F2 | held | not touched: the prompt is unchanged and no criteria or override were added on the model's urgency. |
| F3 | held | not touched: a summary the model gives is still used as before. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the same closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the same closed list is still checked by code. |
| C3 | moved toward the charter | `+ if queue is None: fallback.append("queue")` marks each invalid field while the others keep their value. Only in part: `+ queue = "general"` and `+ urgency = "normal"` still put a default where the line says `null`. |
| C4 | held | not touched: the tier is still absent from the prompt, and the enterprise raise is the same code, applied after the defaults as before. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged; the missing `null` hours follow from the C3 gap, which the change did not widen. |
| C6 | held | `+ summary = subject` replaces `or subject` with the same behaviour; `summary[:MAX_SUMMARY_CHARS]` and the whitespace join are unchanged. |
| C7 | held | not touched: one `model(...)` call, `body[:MAX_BODY_CHARS]`, no retry or chunking. |
| C8 | held | not touched: the `ValueError` guard, the `FIELD` regex, `setdefault` and the stripping in `_choice` are unchanged. |
| B1 | held | not touched: one model call per ticket, body cap still 2000. |

## Trial

- where: code
- flagged: no
- stopped: no
