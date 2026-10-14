## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap the line names (code keeps only attendee names) is as it was. |
| F4 | held | `+ The days from the meeting day for the next two weeks are: {calendar}` and `+ is converted to a date using the days listed above`: the calendar is context and the model still reads "next week" and picks the date. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still rejects non-dates and dates before the meeting. |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS` still caps at 10, so the gap is as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one model call, no retry, and the same parsing and skipping. |
| B1 | held | not touched; still one model call per set of notes. |

## Trial

- where: prompt
- flagged: no
- stopped: no