## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | Prompt not touched; the model still judges urgency with no criteria fixed in code. The removed override is judged under C4. |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched; `_choice(fields.get("urgency"), URGENCIES, "normal")` still limits urgency to the four levels. |
| C3 | held | not touched; `"general"` and `"normal"` defaults remain, and `+ deadline_level = urgency` leaves the gap as it was. |
| C4 | moved toward the model | `- urgency = URGENCIES[level]` replaced by `+ deadline_level = URGENCIES[level]`: code no longer raises enterprise urgency, so the model's level passes as final. The tier still does not reach the model. |
| C5 | moved toward code | `- RESPOND_WITHIN_HOURS[urgency]` to `+ RESPOND_WITHIN_HOURS[deadline_level]`: a tier rule is added, so hours no longer come from the returned urgency (enterprise `high` gives 1). |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched; still one model call, body cut at `MAX_BODY_CHARS`. |

## Trial

- where: code
- flagged: no
- stopped: no