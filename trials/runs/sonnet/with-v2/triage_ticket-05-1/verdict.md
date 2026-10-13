## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code; the only other value is the `null` that C3 requires. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership is still checked by code; the only other value is the `null` that C3 requires. |
| C3 | moved toward the charter | `- return value if value in allowed else default` / `+ return value if value in allowed else None`: the `general` and `normal` defaults are gone, and each field is nulled independently. |
| C4 | held | `+ if urgency is not None and ticket.get("tier") == "enterprise":`: the tier still never reaches the prompt and code still raises one level; the guard only skips a `null` urgency, which has no level to raise. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: hours still come from the urgency table, and are `null` when the urgency is `null`, as the line says. |
| C6 | held | not touched: `summary = " ".join(...) or subject` and the 120-character cut are unchanged. |
| C7 | held | not touched: one model call, body cut at `MAX_BODY_CHARS`, no retry added. |
| C8 | held | not touched: the `ValueError`, the `FIELD` regex and first-occurrence parsing are unchanged; `_choice` keeps its `.strip(" .*`\"'").lower()` normalization. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
