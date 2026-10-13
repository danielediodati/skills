## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the prompt is unchanged and the model still picks the queue. |
| F2 | held | not touched: no urgency criteria or rule added in prompt or code. |
| F3 | held | not touched: the summary text is still the model's; `defaulted` only records its absence. |
| C1 | held | `+ queue = _choice(fields.get("queue"), QUEUES)` then `+ queue = queue or "general"`: the result is still always one of the five queues. |
| C2 | held | `+ urgency = _choice(fields.get("urgency"), URGENCIES)` then `+ urgency = urgency or "normal"`: the result is still always one of the four levels. |
| C3 | moved toward the charter | `+ defaulted = [name for name, value in ... if not value]` and `+ "needs_review": bool(defaulted)`: a default no longer shows as decided. Partial: `+ queue = queue or "general"` still puts a default, not `null`. |
| C4 | held | not touched: the tier is still absent from the prompt and the enterprise raise is unchanged. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged; the missing `null` case follows from the C3 gap, which the change did not widen. |
| C6 | held | `+ summary = summary or subject` with `summary[:MAX_SUMMARY_CHARS]` unchanged: same one line, same cap, same subject fallback, only reordered. |
| C7 | held | not touched: one model call, body cut at `MAX_BODY_CHARS`, no retry. |
| C8 | held | `+ return value if value in allowed else None`: the stripping and lowercasing are kept; `_parse_fields` and the `ValueError` are untouched. |
| B1 | held | not touched: one call per ticket, body up to the cap. |

## Trial

- where: code
- flagged: no
- stopped: no
