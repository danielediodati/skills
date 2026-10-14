## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (code keeps only attendees) is as before |
| F4 | held | `+ "by Friday" is the first Friday on or after that date ... "end of next week" is the Friday of that week.`: a definition of how to read a phrase; the model still works out the date from the notes. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still checks real date and `>= meeting_date` |
| C3 | held | not touched; rejected dates still become `None`, as before |
| C4 | held | not touched |
| C5 | held | not touched; the cap of 10 is as before |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; one call, same parsing, same `NONE` handling |
| B1 | held | not touched; still one model call per set of notes |

## Trial

- where: prompt
- flagged: no
- stopped: no