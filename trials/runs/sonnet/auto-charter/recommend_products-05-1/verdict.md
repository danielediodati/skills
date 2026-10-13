## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ so write it to fit: a complete thought, not a longer one trimmed.`: tells the model the display limit; the model still decides what each reason says. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+ max_reason=MAX_REASON_CHARS,` only feeds the prompt; the `[:MAX_REASON_CHARS]` cut and the kept empty reason are unchanged. |
| C6 | held | not touched: still one `model(...)` call; a retry is only offered as an option, not made. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial
