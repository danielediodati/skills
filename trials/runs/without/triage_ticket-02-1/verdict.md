## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code; only the default argument left `_choice`. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code. |
| C3 | moved toward the charter | `+ if queue is None: queue = "general"; fallbacks.append("queue")` (same for urgency): the default is still put in place of `null`, but the result now names it as not classified. Gap closed in part. |
| C4 | held | not touched: the tier still stays out of the prompt and code still raises `enterprise` one level, now also on a flagged stand-in `normal` as before. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` unchanged; urgency is still never `null`, as before. |
| C6 | held | `+ if not summary: summary = subject; fallbacks.append("summary")`: still the subject when the model gives none, still one line cut to 120. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
