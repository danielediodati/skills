## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ "summary": _shorten(summary, MAX_SUMMARY_CHARS),`: code only cuts the model's own words at a word or sentence boundary and adds `…`; the prompt is unchanged and the wording stays the model's. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | `+ room = limit - len(ELLIPSIS)` and `+ if m.end() + 1 <= room`: the result is still one line of at most 120 characters, cut by code; `or subject` is unchanged. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
