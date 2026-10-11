## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code. |
| C3 | moved toward the charter | `+ return value if value in allowed else None` replaces `else default`: an invalid field is now `null`, and the other fields keep their value. |
| C4 | held | `+ if urgency is not None and ticket.get("tier") == "enterprise":`: code still raises enterprise one level, and the tier still never reaches the model. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: hours still come from the urgency, and are `null` when the urgency is `null`. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
