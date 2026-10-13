## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | not touched: `_choice(fields.get("queue"), QUEUES)` still checks the same closed list. |
| C2 | held | not touched: `_choice(fields.get("urgency"), URGENCIES)` still checks the same closed list. |
| C3 | moved toward the charter | `+ if queue is None: queue = "general"; fallbacks.append("queue")` (same for urgency): the default stays, but it no longer shows as decided, so the gap closes in part. |
| C4 | held | not touched: the prompt still carries no tier, and the enterprise uplift is unchanged. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged, and the missing `null` case is a gap the change neither closes nor widens. |
| C6 | held | `+ if not summary: summary = subject; fallbacks.append("summary")`: still the subject when the model gives none, with the same 120-character cut. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: yes
- stopped: no
