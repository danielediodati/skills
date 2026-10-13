## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name kept, anyone else `None`) is as it was. |
| F4 | held | `+ {calendar}` and `+ resolve them against the calendar above`: code supplies weekday-to-date pairs, not answers. The model still reads which Friday and what "end of next week" means. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; a rejected date and one never given are both still `None`, the gap as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `return items[:MAX_ITEMS]` is unchanged, the gap as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, and the calendar is built without a call. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no