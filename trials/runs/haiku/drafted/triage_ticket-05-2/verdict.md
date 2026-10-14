## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| C1 | held | `_choice(...)` still returns a value only if it is in `QUEUES`, otherwise `None` and then `queue or "general"`: the list is checked as before. |
| C2 | held | `_choice(fields.get("urgency"), URGENCIES)` still validates against the closed list; not otherwise touched. |
| C3 | held | `queue = queue or "general"` / `urgency = urgency or "normal"` still put defaults where the line says `null`; the added `judged` flag marks the default but leaves the gap as it was. |
| C4 | held | Enterprise bump block and prompt are unchanged; `judged` is computed before the bump and the tier still never reaches the model. |
| C5 | held | `RESPOND_WITHIN_HOURS[urgency]` is unchanged and still derived from the urgency by code. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no