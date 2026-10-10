## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ "summary": _shorten(summary, MAX_SUMMARY_CHARS),`: code only cuts the model's own words to fit the space and adds `…`; the prompt is unchanged and the model still writes the summary. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: the `general` and `normal` defaults are as before, so the gap is neither closed nor widened. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | `+ room = limit - len(ELLIPSIS)` and `+ return kept + ELLIPSIS`: the result is still one line of at most 120 characters, marker included; the subject fallback is unchanged. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
