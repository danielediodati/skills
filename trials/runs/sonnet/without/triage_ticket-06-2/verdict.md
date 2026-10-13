## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ body = _redact(ticket.get("body", "")).strip()`: secrets become placeholders before the model reads, but it still sees what the customer needs and picks the queue itself. |
| F2 | held | Same input redaction; no urgency criteria or rule added in prompt or code, so the judgement stays the model's. |
| F3 | moved toward code | `+ summary = " ".join(_redact(fields.get("summary", "")).split()) or subject`: regex override applied to the model's summary, e.g. "password is wrong" becomes "password is [removed]". The prompt addition "without card numbers, security codes, passwords" alone would only be a criterion. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general` and `normal` defaults remain, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | moved toward code | `+ subject = _redact(ticket.get("subject", "")).strip()`: the fallback is no longer the subject in the customer's own words but one rewritten by an added rule. One line and the 120 cap are unchanged. |
| C7 | held | Still one call with `body[:MAX_BODY_CHARS]`, no chunking or retry; the redaction runs before the cut and the cap is unchanged. |
| C8 | held | `_redact` only substitutes placeholders, so an empty ticket still raises `ValueError` before the call; `FIELD` and `_parse_fields` not touched. |
| B1 | held | not touched: one model call, cap still 2000. |

## Trial

- where: both
- flagged: no
- stopped: no