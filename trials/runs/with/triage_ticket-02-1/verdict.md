## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched: the model's summary text is used as before; `stand_in` only reports when it is missing. |
| C1 | held | `+ return value if value in allowed else None`: membership in `QUEUES` is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in `URGENCIES` is still checked by code. |
| C3 | moved toward the charter | `- _choice(fields.get("queue"), QUEUES, "general")` / `+ return value if value in allowed else None`: the defaults are gone, an invalid field is `null` and the others keep their value. |
| C4 | held | `+ if urgency and ticket.get("tier") == "enterprise":`: code still raises one level up to `urgent`, and the tier is still not in the prompt. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: same table, and `null` when the urgency is `null`. |
| C6 | held | `+ "summary": (summary or subject)[:MAX_SUMMARY_CHARS],`: still one line, capped at 120, the subject when the model gives none. |
| C7 | held | not touched: one call, `body[:MAX_BODY_CHARS]`, no retry or chunking added. |
| C8 | held | not touched: the `ValueError` check, `FIELD` and `_parse_fields` are unchanged. |
| B1 | held | not touched: still one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: no
- stopped: no
