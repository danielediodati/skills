## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code, and the output is still one of the five queues. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code, and the output is still one of the four levels. |
| C3 | moved toward the charter | `+ if queue is None: queue = "general"` / `+ fallbacks.append("queue")` (same for urgency): the defaults stay where the line says `null`, but an unclassified field no longer shows as decided, so the gap closes in part. |
| C4 | held | not touched: the tier is still absent from the prompt and the `enterprise` raise is unchanged. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged, and urgency is still never `null` in code. |
| C6 | held | `+ if not summary: summary = subject` / `+ fallbacks.append("summary")`: still one line, capped at 120, the subject when the model gives none; the change only reports it. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
