## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | The model still picks the queue; the added prompt text "base the answer on what the customer is asking for now" is a criterion that informs its judgement. The input cutting is judged under C7. |
| F2 | held | The model still sets the urgency; the new prompt note fixes no level, and the input cutting is judged under C7. |
| F3 | held | The model still writes the summary; not touched beyond the shared prompt note. |
| C1 | held | not touched: `QUEUES` and `_choice(fields.get("queue"), QUEUES, "general")` are unchanged. |
| C2 | held | not touched: `URGENCIES` and its `_choice` check are unchanged. |
| C3 | held | not touched: the `"general"` and `"normal"` defaults stay as before, so the gap is neither closed nor widened. |
| C4 | held | not touched: the prompt is still built from `subject` and `body` only, and the enterprise raise is untouched. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged. |
| C6 | held | not touched: the summary whitespace join, `or subject` fallback and `[:MAX_SUMMARY_CHARS]` cut are unchanged. |
| C7 | moved toward code | `+ body = _fit(_strip_quotes(...))`: code now removes `>` lines, "On … wrote:" blocks and everything after "Original Message" or "From:/Sent:" headers by pattern, then keeps head and tail with `[...]`. The line allows a body cut to a fixed cap, not code choosing by content which text the model reads. |
| C8 | held | The empty-ticket `ValueError` before the model call is kept, and `_strip_quotes(...) or body` never turns a non-empty body into an empty one. `_parse_fields` is untouched. |
| B1 | held | `-MAX_BODY_CHARS = 2000` / `+MAX_BODY_CHARS = 6000` is a budget number, and there is still one model call. |

## Trial

- where: both
- flagged: no
- stopped: no