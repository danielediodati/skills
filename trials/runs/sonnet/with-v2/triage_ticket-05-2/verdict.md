## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched; the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched; no urgency criteria were added in code or prompt. |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code. |
| C3 | moved toward the charter | `- return value if value in allowed else default` / `+ return value if value in allowed else None`: the `general` and `normal` defaults are gone, each field judged on its own. |
| C4 | held | `+ if urgency is not None and ticket.get("tier") == "enterprise":`: code still raises one level, a `null` urgency stays `null`, and the tier is still absent from the prompt. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: hours still come from the urgency, and are `null` when the urgency is `null`, as the line says. |
| C6 | held | not touched; `summary = ... or subject` and the 120-character cut are unchanged. |
| C7 | held | not touched |
| C8 | held | not touched; `_parse_fields`, the `FIELD` pattern and the `ValueError` are unchanged. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
