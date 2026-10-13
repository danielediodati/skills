## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: the prompt is unchanged and no urgency criteria were added in code. |
| F3 | held | not touched: the summary text is still the model's. |
| C1 | held | `+ return value if value in allowed else None`: membership in `QUEUES` is still checked by code, as before. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)`: membership in `URGENCIES` is still checked by code, as before. |
| C3 | moved toward the charter | `+ "defaulted": defaulted` names the fields not validly given, so a default no longer shows as decided. Partial only: `+ queue = queue or "general"` and `+ urgency = urgency or "normal"` still put the defaults instead of `null`. |
| C4 | held | not touched: the tier is still absent from the prompt, and the enterprise block is unchanged context in the diff. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged. Urgency is still never `null` in the output, the same gap as before. |
| C6 | held | `+ summary = summary or subject` keeps the subject fallback, moved but equivalent; `summary[:MAX_SUMMARY_CHARS]` is unchanged. |
| C7 | held | not touched: one `model(...)` call, `body[:MAX_BODY_CHARS]`, no retry. |
| C8 | held | not touched: the `ValueError`, `FIELD`, `_parse_fields` and the stripping in `_choice` are unchanged. |
| B1 | held | not touched: one model call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: no
- stopped: no
