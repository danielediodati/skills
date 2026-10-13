## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue; `fell_back` only reports. |
| F2 | held | not touched: no urgency criteria or rule added; `+ fell_back.append("urgency")` records, it does not decide. |
| F3 | held | not touched: the model's summary is used as before. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code. |
| C3 | moved toward the charter | `+ if queue is None: queue = "general"; fell_back.append("queue")` (same for urgency): the default stays, but an unclassified field no longer shows as decided. Gap closed in part. |
| C4 | held | not touched: the tier stays out of the prompt and `if ticket.get("tier") == "enterprise":` still raises one level, capped at `urgent`. |
| C5 | held | not touched: `"respond_within_hours": RESPOND_WITHIN_HOURS[urgency]` is unchanged; hours for a defaulted urgency are as before. |
| C6 | held | `+ if not summary: summary = subject; fell_back.append("summary")`: still the subject when the model gives none, one line, cut to 120. |
| C7 | held | not touched: one call, body cut at `MAX_BODY_CHARS`, no retry or merge. |
| C8 | held | not touched: the `ValueError`, `FIELD`, `_parse_fields` and the stripping in `_choice` are unchanged. |
| B1 | held | not touched: one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: yes
- stopped: no
