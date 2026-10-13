## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only an attendee's name is kept, anyone else becomes `None`) is as it was. |
| F4 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; a rejected date and one never given are both still `None`. |
| C4 | held | not touched |
| C5 | moved toward the charter | `+ return items[:MAX_ITEMS], items[MAX_ITEMS:]` and `+ warnings.warn(`: items past the cap are now returned and announced, closing the gap in part. `extract_action_items` still keeps 10. |
| C6 | held | not touched |
| C7 | held | not touched; the `items.sort(...)` line is unchanged and `omitted` is the tail of the same sorted list. |
| C8 | held | `+ return [], []` and `+ items, omitted = extract_with_omitted(notes, attendees, meeting_date, model)`: still one call, and empty notes still return without calling the model. |
| B1 | held | not touched; the wrapper delegates once, so there is still one model call per set of notes. |

## Trial

- where: code
- flagged: yes
- stopped: no
