## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched: the model's summary text is used as before. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code. |
| C3 | moved toward the charter | `+ if queue is None: queue = "general"; fallbacks.append("queue")` (same for urgency): the default stays instead of `null`, but it no longer shows as decided. Gap closed in part. |
| C4 | held | not touched: the tier is still absent from the prompt, and the enterprise raise is unchanged. |
| C5 | held | not touched: `"respond_within_hours": RESPOND_WITHIN_HOURS[urgency]` is unchanged; it is still 24 rather than `null` for an unjudged urgency, as before. |
| C6 | held | `+ if not summary: summary = subject; fallbacks.append("summary")`: still the subject when the model gives none, still one line cut to 120. |
| C7 | held | not touched: one model call, body cut to `MAX_BODY_CHARS`, no retry. |
| C8 | held | not touched: the `ValueError`, `FIELD` and `_parse_fields` are unchanged; `_choice` strips and lowercases as before. |
| B1 | held | not touched: one call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: yes
- stopped: no
