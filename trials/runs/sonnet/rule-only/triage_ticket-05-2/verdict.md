## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue; `+ queue = "general"` is the same fallback as before. |
| F2 | held | not touched: the prompt is unchanged and the model still judges urgency; `+ urgency = "normal"` is the same fallback as before. |
| F3 | held | not touched: the model's summary text is used as before; `+ unjudged.append("summary")` only labels the subject fallback. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES, None)`: membership in the closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES, None)`: membership in the closed list is still checked by code. |
| C3 | moved toward the charter | `+ if queue is None:` / `+ queue = "general"` / `+ unjudged.append("queue")`: the default stays instead of `null`, but it no longer shows as decided. Gap closed in part only. |
| C4 | held | not touched: the tier is still absent from the prompt and `if ticket.get("tier") == "enterprise":` still raises one level, capped at `urgent`. |
| C5 | held | not touched: `"respond_within_hours": RESPOND_WITHIN_HOURS[urgency]` is unchanged; urgency is still never `null`, a gap the change did not create. |
| C6 | held | `+ if not summary:` / `+ summary = subject`: same subject fallback, still one line and cut by `summary[:MAX_SUMMARY_CHARS]`. |
| C7 | held | not touched: one `model(...)` call, `body[:MAX_BODY_CHARS]`, no retry or chunking. |
| C8 | held | not touched: the `ValueError` check, `FIELD` and `_parse_fields` are unchanged. |
| B1 | held | not touched: one model call per ticket, body cap unchanged. |

## Trial

- where: code
- flagged: yes
- stopped: no
