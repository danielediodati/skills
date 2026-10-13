## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+The reason must be a complete sentence of at most {max_chars} characters`: sets form and length, which informs the model; what the reason says is still the model's choice. |
| F5 | held | not touched; the added prompt line does not fix the language of the reason. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+        max_chars=MAX_REASON_CHARS,` only tells the model the limit; the cut `[:MAX_REASON_CHARS]` and the kept empty reason are unchanged. |
| C6 | held | not touched; still one `model(...)` call, and the retry is only named as an option, not made. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per search. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
