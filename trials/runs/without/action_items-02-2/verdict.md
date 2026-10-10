## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is left as it was. |
| F4 | moved toward code | `+  A day of the week is a deadline: "by Friday" is the first Friday after the meeting (a week later if the meeting itself is on a Friday)` dictates the reading in the prompt. `+ due = _weekday_due(text, meeting_date)` then resolves weekday phrases by a fixed rule in code. |
| C1 | held | not touched |
| C2 | held | `+    return due if due >= meeting_date else None`: a date resolved from a weekday still passes the same check, and anything else still fails `date.fromisoformat`. |
| C3 | held | `+        if due is None:` / `+            return None`: a rejected date still becomes `None`, the same as one never given; the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS = 10` is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; the added `calendar=` and `meeting_weekday=` only build the single prompt. |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: both
- flagged: no
- stopped: no
