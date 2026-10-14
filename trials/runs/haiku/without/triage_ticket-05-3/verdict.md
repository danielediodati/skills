## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `queue = _choice(fields.get("queue"), QUEUES)` still accepts only a name in `QUEUES`. |
| C2 | held | `urgency = _choice(fields.get("urgency"), URGENCIES)` still accepts only a name in `URGENCIES`. |
| C3 | held | `_choice(..., default=None)` is followed by `queue = queue or "general"` and `urgency = urgency or "normal"`, so the defaults are still put. The `judged` flag only reports them, so the gap is as before. |
| C4 | held | The enterprise bump block is moved but its logic is unchanged, and the prompt is untouched. |
| C5 | held | `RESPOND_WITHIN_HOURS[urgency]` is unchanged, and the gap on `null` is as before. |
| C6 | held | `summary = summary or subject` and `summary[:MAX_SUMMARY_CHARS]` keep the one-line, 120-character, subject-fallback rule. |
| C7 | held | not touched; still one call and the same `body[:MAX_BODY_CHARS]` cut. |
| C8 | held | not touched; the empty-ticket check and `_parse_fields` are unchanged. |
| B1 | held | not touched. |

## Trial

- where: code
- flagged: no
- stopped: no