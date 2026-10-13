## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | `+ work out whether the day or the month comes first from the evidence on the invoice`: criteria that inform; the model still picks the date and sets the flag that `+ if ambiguous:` acts on. |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward code | `+ if not isinstance(ambiguous, bool): raise InvoiceError("issue_date_ambiguous is missing")` and `+ if ambiguous: raise InvoiceError(...)`: a required key and a refusal rule beyond the shape the line names. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is still the amount due) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call; the ambiguous case raises, with no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: yes
- stopped: no