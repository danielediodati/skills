## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | `+  urgent = something is broken for the customer right now...` adds criteria that inform the model's judgement; the charter says criteria go in the prompt. The model still reads each ticket and picks the level. |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; `_choice(..., "general")` and `_choice(..., "normal")` defaults remain, so the gap is as before. |
| C4 | moved toward code | `- level = min(URGENCIES.index(urgency) + 1, ...)` is removed and `+ deadlines = ENTERPRISE_RESPOND_WITHIN_HOURS` added: the enterprise raise is replaced by a different code rule keyed on tier. The tier still never reaches the model. |
| C5 | moved toward code | `+ ENTERPRISE_RESPOND_WITHIN_HOURS = {"low": 24, "normal": 8, "high": 8, "urgent": 1}`: hours now depend on tier as well as urgency, where the line says they come from the urgency (72, 24, 8, 1). |
| C6 | held | not touched |
| C7 | held | not touched; still one call and `body[:MAX_BODY_CHARS]`. |
| C8 | held | not touched |
| B1 | held | not touched; one call with the body cut to the cap. The prompt is longer but there is still one call. |

## Trial

- where: both
- flagged: no
- stopped: no