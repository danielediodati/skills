## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code; only the fallback changed. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code; only the fallback changed. |
| C3 | moved toward the charter | `+ return value if value in allowed else None` replaces `else default`: an invalid field is now `null`, and the other fields keep their value. |
| C4 | held | `+ if urgency is not None and ticket.get("tier") == "enterprise":`: the tier still stays out of the prompt and code still raises one level; a `null` urgency is left `null`. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: hours still come from the urgency table, and are `null` when the urgency is `null`. |
| C6 | held | `+ summary = summary or subject` with `summary[:MAX_SUMMARY_CHARS]` unchanged: still one line, capped at 120, the subject when the model gives none. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
