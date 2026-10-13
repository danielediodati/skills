## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | not touched: `_choice(fields.get("queue"), QUEUES)` still accepts only the five queues. |
| C2 | held | not touched: `_choice(fields.get("urgency"), URGENCIES)` still accepts only the four levels. |
| C3 | moved toward the charter | `+ if queue is None: queue = "general"` / `+ fallback_fields.append("queue")`: the field is still a default, not `null`, but the output now names it as not classified. The gap closes in part. |
| C4 | held | not touched |
| C5 | held | not touched: `"respond_within_hours": RESPOND_WITHIN_HOURS[urgency]` is unchanged. |
| C6 | held | `+ if not summary: summary = subject`: same fallback to the subject as before, and `summary[:MAX_SUMMARY_CHARS]` is unchanged. |
| C7 | held | not touched |
| C8 | held | `+ return value if value in allowed else None`: the answer is read the same way, and only the miss value changes. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
