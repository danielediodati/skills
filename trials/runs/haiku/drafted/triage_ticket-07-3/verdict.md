## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | `+ Urgency is how soon a person must act: - urgent: something is broken for the customer right now...`: criteria that inform the model's judgement, which the charter says belong in the prompt. The model still reads each ticket and picks the level. |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched; the prompt's four levels are the same closed list. |
| C3 | held | not touched; `_choice(..., "general")` and `_choice(..., "normal")` still put defaults where the line says `null`, and the change neither widens nor narrows that gap. |
| C4 | held | not touched; the enterprise raise stays in code and the tier still does not reach the prompt. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched; still one call and the same body cap. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: no