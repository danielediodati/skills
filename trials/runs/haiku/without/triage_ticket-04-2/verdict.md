## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | The prompt addition "Route and summarise on what they are asking for now, not on the first thing they wrote" is criteria; the model still picks the queue. |
| F2 | held | The urgency judgement is still the model's; the added prompt paragraph sets no urgency outcome. |
| F3 | held | The model still writes the summary; the added prompt text only says to summarise on the current request. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `_choice(..., "general")` / `"normal"` defaults the line calls a gap are unchanged. |
| C4 | held | not touched; the tier is still not in the prompt and the enterprise raise is unchanged. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | moved toward code | `- body=body[:MAX_BODY_CHARS]` → `+ body=_shorten(_without_quoted_history(body))`: code now drops `>` lines, "wrote:" headers and everything after an "Original Message" marker, and keeps head 1000 and tail 2000, where the line says the body is cut to a fixed cap. |
| C8 | held | The empty ticket check still raises before the model call and answer parsing is untouched; the new cleaning runs after it. |
| B1 | held | Still one model call; `MAX_BODY_CHARS = 2000` → `3000` is a budget number, which the charter says may be raised. |

## Trial

- where: both
- flagged: no
- stopped: no