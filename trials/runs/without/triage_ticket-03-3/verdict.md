## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ "summary": _shorten(summary, MAX_SUMMARY_CHARS),`: code still only cuts the model's own words to fit and marks the cut with `…`. The prompt is unchanged and nothing is rewritten. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults remain as before, so the gap is neither closed nor widened. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | `+ if len(candidate) + len(" " + ELLIPSIS) > limit: break` and `+ room = limit - len(ELLIPSIS)`: the result is still one line of at most 120 characters, the `…` included. The `or subject` fallback is unchanged. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
