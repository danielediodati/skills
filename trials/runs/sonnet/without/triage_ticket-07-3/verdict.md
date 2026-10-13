## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched: the prompt is unchanged and the model still judges urgency with no criteria fixed in code. |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | moved toward the model | `- level = min(URGENCIES.index(urgency) + 1, len(URGENCIES) - 1)` and `- urgency = URGENCIES[level]` removed on purpose: the enterprise urgency is now the model's answer unraised. The tier still does not reach the model. |
| C5 | moved toward code | `+ ENTERPRISE_RESPOND_WITHIN_HOURS = {"low": 24, "normal": 8, "high": 4, "urgent": 1}` and `+ "respond_within_hours": deadlines[urgency]`: a second lookup table keyed on tier, with a 4-hour value the line does not have. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no