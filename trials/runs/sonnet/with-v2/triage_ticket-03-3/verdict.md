## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ "summary": _fit(summary, MAX_SUMMARY_CHARS)`: code only drops the tail of the model's own words and appends `…`. The prompt is unchanged, so the wording is still the model's. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched: `_choice(..., "general")` and `_choice(..., "normal")` remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | `- "summary": summary[:MAX_SUMMARY_CHARS]` / `+ "summary": _fit(summary, MAX_SUMMARY_CHARS)`: still one line, never over 120 with the marker. The subject fallback `or subject` is unchanged. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
