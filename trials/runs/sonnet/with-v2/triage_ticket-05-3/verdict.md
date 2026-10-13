## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue; code only stops substituting `general`. |
| F2 | held | not touched: the prompt is unchanged and the model still judges urgency; code only stops substituting `normal`. |
| F3 | held | not touched |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)`: membership in the closed list is still checked by code; the only other value is the `null` that C3 requires. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in the closed list is still checked by code; the only other value is the `null` that C3 requires. |
| C3 | moved toward the charter | `- return value if value in allowed else default` / `+ return value if value in allowed else None`: an invalid field is now `null`, never `general` or `normal`, and each field is handled on its own. |
| C4 | held | `+ if urgency is not None and ticket.get("tier") == "enterprise":`: code still raises enterprise one level up to `urgent`, a `null` urgency stays `null`, and the tier still never reaches the prompt. |
| C5 | held | `+ "respond_within_hours": RESPOND_WITHIN_HOURS.get(urgency),`: hours still come from the urgency (72, 24, 8, 1) and are `null` when the urgency is `null`. |
| C6 | held | not touched: `summary = " ".join(fields.get("summary", "").split()) or subject` and the 120-character cut are unchanged. |
| C7 | held | not touched: one model call, body cut to `MAX_BODY_CHARS`, no retry or chunking added. |
| C8 | held | not touched: the `ValueError` before the call, the `FIELD` pattern and `setdefault` (first occurrence wins) are unchanged. |
| B1 | held | not touched: still one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: no
- stopped: no
