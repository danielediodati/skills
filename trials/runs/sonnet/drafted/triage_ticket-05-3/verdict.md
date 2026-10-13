## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `+ return value if value in allowed else None`: membership in the closed list is still checked by code; the output queue is still one of the five. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership is still checked by code; the output urgency is still one of the four. |
| C3 | moved toward the charter | `+ if queue is None: queue = "general"` / `+ defaulted.append("queue")`: the defaults stay instead of `null`, but an unclassified field is now marked and no longer shows as decided. The gap closes in part. |
| C4 | held | not touched: the prompt still carries no tier, and the enterprise raise is unchanged. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged, and the urgency is still never `null`. |
| C6 | held | `+ if not summary: summary = subject`: the same subject fallback, with the one-line join and the 120 cap unchanged. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no