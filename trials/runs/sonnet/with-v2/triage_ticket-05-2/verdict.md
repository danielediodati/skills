## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: no urgency criteria or rules added; the enterprise raise is the same contract rule as before. |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: still checked against the same closed list. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: still checked against the same closed list. |
| C3 | moved toward the charter | `+ return value if value in allowed else None` replaces `else default`; `general` and `normal` are gone, and each field is judged on its own. |
| C4 | held | `+ if urgency is not None and ticket.get("tier") == "enterprise":`: tier still stays out of the prompt, and code raises one level only when there is an urgency to raise. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: same table of 72, 24, 8, 1, and `null` when the urgency is `null`. |
| C6 | held | not touched: `summary = ... or subject` and `[:MAX_SUMMARY_CHARS]` are unchanged. |
| C7 | held | not touched: one call, body cut at `MAX_BODY_CHARS`, no retry added for invalid answers. |
| C8 | held | not touched: the `ValueError`, `FIELD` and `_parse_fields` are unchanged; `_choice` keeps its strip and lower. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
