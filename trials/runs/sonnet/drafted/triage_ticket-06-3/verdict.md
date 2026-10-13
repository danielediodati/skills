## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ it must not repeat private details from the message... Name the kind of thing instead of its value.`: a general rule the model applies by reading each message; the wording stays the model's. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap (`general` and `normal` as defaults) is left as it was. |
| C4 | held | not touched; the added prompt text does not mention the tier. |
| C5 | held | not touched |
| C6 | held | not touched; the 120-character cut and the subject fallback are unchanged, and no code filter was added to the summary. |
| C7 | held | not touched; still one call, body cut at `MAX_BODY_CHARS`, no retry. |
| C8 | held | not touched |
| B1 | held | not touched; one model call per ticket, the cap unchanged. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial