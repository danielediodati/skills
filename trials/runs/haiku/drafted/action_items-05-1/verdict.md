## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the owner gap stays as it was. |
| F4 | held | not touched |
| C1 | held | not touched; items without owner or due still stay in the list. |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; the gap stays as it was. |
| C4 | held | not touched; `_clean_task` is unchanged. |
| C5 | held | `+ return Extraction(items[:MAX_ITEMS], max(0, len(items) - MAX_ITEMS))`: the cap of 10 is kept and only counted, so the gap is neither closed nor widened. |
| C6 | held | not touched |
| C7 | held | not touched; the sort is unchanged. |
| C8 | held | `+ return Extraction([], 0)` on empty notes, and the wrapper returns `.items` (`[]`). The model is still called once and no retry was added. |
| B1 | held | not touched; still one model call. |

## Trial

- where: code
- flagged: yes
- stopped: no