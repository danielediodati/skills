## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ "summary": _fit(summary, MAX_SUMMARY_CHARS),` only shortens the model's own words at a sentence or word boundary and adds `…`. The prompt is unchanged and code writes no content. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | `+ room = limit - len(ELLIPSIS)` and `- "summary": summary[:MAX_SUMMARY_CHARS],`: the mark counts inside the 120, so the summary is still one line of at most 120 characters. The subject fallback `or subject` is unchanged. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
