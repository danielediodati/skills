## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; owner handling (`by_name.get(_key(fields[1]))`) is unchanged, so the gap stays as it was. |
| F4 | held | not touched |
| C1 | held | not touched; items without owner or due still stay in `items`. |
| C2 | held | not touched; `_parse_due` is unchanged. |
| C3 | held | not touched; `_parse_due` still returns `None` for both rejected and absent dates. |
| C4 | held | not touched; `_clean_task` is unchanged. |
| C5 | moved toward the charter | `- MAX_ITEMS = 10` and `- return items[:MAX_ITEMS]` / `+ return Extraction(items, skipped)`: the cap is removed. |
| C6 | held | not touched; the `seen` set comparison is unchanged. |
| C7 | held | not touched; the sort is unchanged. |
| C8 | held | Empty notes still skip the model, and unreadable lines are still left out of `items` (`+ skipped.append(line)`). `NONE` still gives no items and there is still one call. |
| B1 | held | not touched; still a single `model(prompt)` call. |

## Trial

- where: code
- flagged: yes
- stopped: no