## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ "summary": _shorten(summary, MAX_SUMMARY_CHARS),`: code still only cuts the model's text to fit, now at a sentence or word boundary with a `...` marker; the wording stays the model's and the prompt is unchanged. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general` and `normal` defaults are left as they were, so the gap is neither closed nor widened. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | `+ if len(candidate) + 1 + len(ELLIPSIS) > limit: break` and `+ room = limit - len(ELLIPSIS)`: the marker counts inside the 120, the summary is still one line, and `or subject` is unchanged. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
