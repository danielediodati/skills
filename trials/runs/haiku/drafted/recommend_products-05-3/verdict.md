## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+Each reason must be a complete sentence of under {max_chars} characters, so it ends on its own and never trails off.`: this asks for a form and fixes no content, so the model still decides what the reason says. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | The `[:MAX_REASON_CHARS]` cut and the empty-reason handling are unchanged. The added prompt line only asks the model to write within the cap. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: no
- stopped: no