## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched; the gap (only attendees kept, others set to `None`) is as it was. |
| F4 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; `_parse_due` still returns `None` for both rejected and absent dates. |
| C4 | held | not touched |
| C5 | moved toward the charter | `- MAX_ITEMS = 10` and `- return items[:MAX_ITEMS]` / `+ return items`: the cap is removed, closing the gap. |
| C6 | held | not touched; the dedupe still compares `_key(task), owner`, with only `+ log.info(...)` added. |
| C7 | held | not touched |
| C8 | held | skipping still happens, with only `+ log.warning(...)` added; `NONE` is still skipped, with no extra call or retry. |
| B1 | held | not touched; still one `model(prompt)` call. |

## Trial

- where: code
- flagged: no
- stopped: no