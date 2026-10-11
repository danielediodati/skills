## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap marked "Not yet in code" is left as it was. |
| F4 | held | `+ "by Friday" means the first Friday after the meeting date (a week later if the meeting itself is on a Friday)` and `+ weekday=meeting_date.strftime("%A")`: a definition and the meeting's weekday; the model still works out the date. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still rejects unreal dates and dates before the meeting. |
| C3 | held | not touched; the gap marked "Not yet in code" is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched; the gap marked "Not yet in code" is left as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one `model(prompt)` call, with only `{weekday}` added to the prompt. |
| B1 | held | not touched; one model call per set of notes. |

## Trial

- where: prompt
- flagged: yes
- stopped: no
