## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched: the model's summary text is used as before. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the five queues is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the four levels is still checked by code. |
| C3 | moved toward the charter | `+ if queue is None:` / `+ queue = "general"` / `+ fallbacks.append("queue")` (same for urgency): the default stays instead of `null`, but it no longer shows as decided. Gap closed in part. |
| C4 | held | not touched: the tier is still absent from the prompt and the one-level raise is unchanged. |
| C5 | held | not touched: `"respond_within_hours": RESPOND_WITHIN_HOURS[urgency]` is unchanged. |
| C6 | held | `+ if not summary:` / `+ summary = subject` / `+ fallbacks.append("summary")`: still one line, the subject when none is given, cut to 120. |
| C7 | held | not touched: one model call, body cut to `MAX_BODY_CHARS`, no retry. |
| C8 | held | not touched: the `ValueError`, `_parse_fields` and the stripping in `_choice` are unchanged. |
| B1 | held | not touched: one call per ticket, the cap still 2000. |

## Trial

- where: code
- flagged: no
- stopped: no
