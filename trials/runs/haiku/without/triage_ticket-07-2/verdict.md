## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | `+ urgent means the customer cannot use the product or take payments right now and has no workaround.`: criteria the model applies by reading each ticket, which the line allows in the prompt; the model still picks the level. |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: code still puts `general` and `normal`, and the gap is as it was. |
| C4 | moved toward the model | `- level = min(URGENCIES.index(urgency) + 1, len(URGENCIES) - 1)` / `- urgency = URGENCIES[level]`: the enterprise raise is removed, so the model's urgency passes unraised. The tier still does not reach the model. |
| C5 | moved toward code | `+ ENTERPRISE_RESPOND_WITHIN_HOURS = {"low": 24, "normal": 8, "high": 4, "urgent": 1}` and `hours = ENTERPRISE_RESPOND_WITHIN_HOURS[urgency]`: hours now depend on the tier, where the line has them come from urgency alone (72, 24, 8, 1). |
| C6 | held | not touched |
| C7 | held | the prompt gains a paragraph, but there is still one call and the body is still cut to `MAX_BODY_CHARS`. |
| C8 | held | not touched |
| B1 | held | not touched: still one model call per ticket, body up to the cap. |

## Trial

- where: both
- flagged: no
- stopped: no