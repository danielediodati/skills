## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: code still checks membership in the same closed list. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: code still checks membership in the same closed list. |
| C3 | moved toward the charter | `- return value if value in allowed else default` / `+ return value if value in allowed else None`: the `general` and `normal` defaults are gone, and each field is nulled on its own. |
| C4 | held | `+ if urgency is not None and ticket.get("tier") == "enterprise":`: code still raises one level up to `urgent`, and the tier is still absent from the prompt. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: same 72/24/8/1 table, and `None` when the urgency is `None`, as the line says. |
| C6 | held | not touched: the summary is still one line, capped at 120 characters, with the subject as fallback. |
| C7 | held | not touched: one model call, body cut at 2000 characters, no retry added for invalid answers. |
| C8 | held | not touched: the `ValueError`, the `FIELD` regex and first-occurrence-wins are unchanged; `_choice` still strips decoration and case. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
