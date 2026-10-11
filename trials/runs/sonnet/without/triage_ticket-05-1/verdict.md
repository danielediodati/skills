## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched: the model's summary text is used as before. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code. |
| C3 | moved toward the charter | `+ defaulted = [name for name, value in ... if not value]` and `+ "needs_review": bool(defaulted)` mark an unclassified field in the output. Only in part: `+ queue = queue or "general"` and `+ urgency = urgency or "normal"` keep the defaults where the line says `null`. |
| C4 | held | not touched: the tier is still absent from the prompt and code still raises `enterprise` one level, up to `urgent`. |
| C5 | held | not touched: `"respond_within_hours": RESPOND_WITHIN_HOURS[urgency]` is unchanged. Hours are never `null` only because the C3 default remains, a gap the change did not create. |
| C6 | held | `+ summary = summary or subject` is the same subject fallback, reordered, and `summary[:MAX_SUMMARY_CHARS]` is unchanged. |
| C7 | held | not touched: one model call, body cut to `MAX_BODY_CHARS`, no retry or chunking added. |
| C8 | held | not touched: the `ValueError`, `FIELD` and `_parse_fields` are unchanged; `_choice` cleans the value as before and only its fallback became `None`. |
| B1 | held | not touched: one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: no
- stopped: no
