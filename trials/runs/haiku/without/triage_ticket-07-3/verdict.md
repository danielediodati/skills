## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | The prompt adds criteria (`urgent: the customer's product or service is broken...`, `normal: a routine request (a copy of a document...)`); they inform the model's reading and the model still decides. |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general`/`normal` defaults in `_choice` are unchanged, so the gap is as it was. |
| C4 | moved toward code | `if ticket.get("tier") == "enterprise" and urgency in ("low", "normal")` with `never to urgent`: code now caps enterprise at `high`, where the line raises one level up to `urgent`. |
| C5 | held | not touched; `RESPOND_WITHIN_HOURS[urgency]` is unchanged. |
| C6 | held | not touched |
| C7 | held | not touched; still one call and `body[:MAX_BODY_CHARS]`, only the prompt text grew. |
| C8 | held | not touched |
| B1 | held | not touched; still one model call per ticket with the body up to the cap. |

## Trial

- where: both
- flagged: no
- stopped: no