## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ Say what the customer needs without repeating private details from the message, such as card numbers, security codes, passwords...`: a criterion in the prompt that the model applies by reading each ticket; the wording of the summary is still the model's. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the gap (`general` and `normal` as defaults) is left as it was. |
| C4 | held | not touched; the added prompt text does not mention the tier. |
| C5 | held | not touched |
| C6 | held | not touched; the one-line join, the 120-character cap and the subject fallback are unchanged. |
| C7 | held | not touched; still one call, body cut at `MAX_BODY_CHARS`, no retry or second pass over the summary. |
| C8 | held | not touched |
| B1 | held | not touched; one model call per ticket, cap unchanged. |

## Trial

- where: prompt
- flagged: yes
- stopped: no