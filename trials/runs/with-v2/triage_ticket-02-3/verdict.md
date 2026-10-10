## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the five queues is still checked by code; only the fallback changed. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the four levels is still checked by code; only the fallback changed. |
| C3 | moved toward the charter | `- return value if value in allowed else default` / `+ return value if value in allowed else None`: invalid queue or urgency is now `null`, other fields keep their value. |
| C4 | held | `+ if urgency is not None and ticket.get("tier") == "enterprise":`: tier still stays out of the prompt, code still raises one level; a `null` urgency is left `null`. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: hours still come from the urgency, and are `null` when the urgency is `null`. |
| C6 | held | `+ summary = summary or subject` with `summary[:MAX_SUMMARY_CHARS]` unchanged: one line, 120 characters, subject when the model gives none. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
