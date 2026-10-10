## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code; the only other value is the `null` that C3 asks for. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code; the only other value is the `null` that C3 asks for. |
| C3 | moved toward the charter | `+ return value if value in allowed else None` replaces `else default`: an invalid queue or urgency is now `null`, and the other fields keep their value. |
| C4 | held | `+ if urgency and ticket.get("tier") == "enterprise":`: code still raises enterprise one level, a `null` urgency has no level to raise, and the prompt still carries no tier. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: hours still come from the urgency in code, and are `null` when the urgency is `null`. |
| C6 | held | `+ summary = subject` when the model gives none, still cut by `summary[:MAX_SUMMARY_CHARS] or None`: the `or None` only turns an empty subject into `null`, and code decided that case before too. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
