## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (`by_name.get(_key(fields[1]))` keeps only attendees) is left as it was. |
| F4 | held | not touched |
| C1 | held | not touched; items without owner or due are still appended, and now none are cut by the cap. |
| C2 | held | not touched |
| C3 | held | not touched; a rejected due date and one never given are both still `None`, the gap left as it was. |
| C4 | held | not touched |
| C5 | moved toward the charter | `- MAX_ITEMS = 10` and `- return items[:MAX_ITEMS]` / `+ return items`: the cap is removed, closing the gap. |
| C6 | held | not touched |
| C7 | held | not touched; the sort line is unchanged, only the slice after it removed. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
