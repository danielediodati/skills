## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (code keeps only attendees) is as it was. |
| F4 | held | `+ - "by Friday" (or any weekday) means the next such day on or after the meeting.` is a rule for reading a phrase, and the plain weekday calendar is a reference the model still reads against; it maps no phrase to a value. |
| C1 | held | not touched |
| C2 | held | not touched; `_parse_due` still rejects non-dates and dates before the meeting. |
| C3 | held | not touched; rejected and absent dates are both still `None`. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS` cap is as before. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched; still one call, blank-notes early return and line filtering unchanged. |
| B1 | held | not touched; the prompt is still sent once. |

## Trial

- where: prompt
- flagged: yes
- stopped: no