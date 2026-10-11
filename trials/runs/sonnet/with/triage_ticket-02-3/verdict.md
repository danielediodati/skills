## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged, and removing the `"general"` fallback takes no queue decision from the model. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched: `stand_ins` only reports a missing summary, it does not change what the summary says. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the five queues is still checked by code; the only other value is the `None` that C3 requires. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the four levels is still checked by code; the only other value is the `None` that C3 requires. |
| C3 | moved toward the charter | `- return value if value in allowed else default` / `+ return value if value in allowed else None`: the `general` and `normal` defaults are gone, and the other fields keep their value. |
| C4 | held | `+ if urgency is not None and ticket.get("tier") == "enterprise":`: code still raises enterprise one level up to `urgent`, and the tier is still absent from the prompt. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: hours still come from the urgency table, and are `None` when the urgency is `None`, as the line says. |
| C6 | held | `+ summary = summary or subject` with `summary[:MAX_SUMMARY_CHARS]` unchanged: still one line, capped at 120, the subject when the model gives none. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
