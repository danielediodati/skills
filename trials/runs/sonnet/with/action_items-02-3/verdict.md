## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: the owner instruction and `by_name.get(...)` are unchanged, so the gap is as it was. |
| F4 | held | `+ A bare weekday ("by Friday") is the first such day after the meeting, never the meeting day itself.`: a definition of how to read a phrase, and the model still works out the date. `+ weekday=_WEEKDAYS[meeting_date.weekday()]` hands over a fact about the meeting, not the answer. |
| C1 | held | not touched |
| C2 | held | not touched: `_parse_due` is unchanged; `-_EMPTY = {` / `+_EMPTY ={` is spacing only. |
| C3 | held | not touched: a rejected date and one never given are both still `None`, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `MAX_ITEMS = 10` and `items[:MAX_ITEMS]` are unchanged, so the gap is as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched: still a single `model(prompt)` call, with the same empty-notes return, line skipping and `NONE` handling. |
| B1 | held | not touched: one model call per set of notes. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
