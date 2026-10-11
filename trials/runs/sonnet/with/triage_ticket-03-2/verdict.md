## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ "summary": _shorten(summary, MAX_SUMMARY_CHARS)`: the prompt is unchanged and the words are still the model's; code only cuts them at a sentence or word to fit the fixed space, as C6 gives it to do. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | `- "summary": summary[:MAX_SUMMARY_CHARS]` becomes `+ "summary": _shorten(summary, MAX_SUMMARY_CHARS)` with `room = limit - len(ELLIPSIS)`: still one line of at most 120 characters, mark included, and the subject is still used when the model gives none. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
