## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+Each reason must be a complete sentence of at most {max_reason} characters, including spaces: it is cut off at that length.` sets form and length, not content: the model still decides what the reason says. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+        max_reason=MAX_REASON_CHARS,` only tells the model the limit; the `[:MAX_REASON_CHARS]` cut and the kept empty reason are unchanged in code. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
