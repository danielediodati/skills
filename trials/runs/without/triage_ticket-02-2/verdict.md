## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched: the model's summary text is used as before. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the same closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the same closed list is still checked by code. |
| C3 | moved toward the charter | `+ if queue is None: queue = "general"; fallbacks.append("queue")` (same for urgency): the default stays instead of `null`, but it no longer shows as decided. The gap closes only in part. |
| C4 | held | not touched: the tier is still absent from the prompt, and the `enterprise` raise is unchanged. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged, and the urgency is still never `null`, as before. |
| C6 | held | `+ if not summary: summary = subject; fallbacks.append("summary")`: the subject still stands in, and the result is still one line cut to `MAX_SUMMARY_CHARS`. |
| C7 | held | not touched: one model call, body cut to `MAX_BODY_CHARS`, no retry and no chunking. |
| C8 | held | not touched: the `ValueError` check, `FIELD` and `_parse_fields` are unchanged. `_choice` strips the same marks and case. |
| B1 | held | not touched: one model call per ticket, same cap. |

## Trial

- where: code
- flagged: no
- stopped: no
