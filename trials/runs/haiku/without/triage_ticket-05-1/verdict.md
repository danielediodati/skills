## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the queue still comes from the model's answer. |
| F2 | held | not touched: the urgency still comes from the model's answer, and the prompt is unchanged. |
| F3 | held | not touched. |
| C1 | held | `value if value in allowed else ""` in `_clean` still admits only the five queues; `general` is still applied afterwards. |
| C2 | held | `_clean(fields.get("urgency"), URGENCIES)` still admits only the four levels; `normal` is still applied afterwards. |
| C3 | held | `+ queue = queue or "general"` / `+ urgency = urgency or "normal"`: the defaults remain where the line wants `null`. The added `judged` flag marks them but does not close the gap. |
| C4 | held | not touched: the tier block is unchanged and the prompt still carries no tier. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged, and it still gives 24 on the `normal` fallback rather than `null`. |
| C6 | held | not touched: the summary cleaning, the `or subject` fallback and the `[:MAX_SUMMARY_CHARS]` cap are unchanged. |
| C7 | held | not touched: one call, body cut at `MAX_BODY_CHARS`, no retry. |
| C8 | held | not touched: the `ValueError` check and `_parse_fields` are unchanged. |
| B1 | held | not touched: one call per ticket, cap unchanged. |

## Trial

- where: code
- flagged: no
- stopped: no