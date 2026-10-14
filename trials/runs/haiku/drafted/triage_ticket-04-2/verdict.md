## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Judge the ticket by what the customer is asking for now, wherever in the body they say it.` is a criterion informing the model's reading; it names no queue, so the model still chooses. |
| F2 | held | The added prompt text sets no urgency levels or outcomes; the model still judges urgency itself. |
| F3 | held | The added text only says to summarise what the customer is asking for now; the summary wording is still the model's. |
| C1 | held | not touched; `_choice(fields.get("queue"), QUEUES, "general")` is unchanged. |
| C2 | held | not touched; `_choice(fields.get("urgency"), URGENCIES, "normal")` is unchanged. |
| C3 | held | not touched; the `general` and `normal` defaults are as before, so the gap is neither closed nor widened. |
| C4 | held | not touched; the prompt does not include the tier and the enterprise raise is unchanged. |
| C5 | held | not touched; `RESPOND_WITHIN_HOURS[urgency]` is unchanged. |
| C6 | held | not touched; the 120-character cap and the `or subject` fallback are unchanged. |
| C7 | held | not touched; still one call with `body[:MAX_BODY_CHARS]`, and the agent did not change the cut. |
| C8 | held | not touched; the empty-ticket `ValueError` and `FIELD`/`_parse_fields` are unchanged. |
| B1 | held | not touched; one model call per ticket, cap still `MAX_BODY_CHARS = 2000`. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial