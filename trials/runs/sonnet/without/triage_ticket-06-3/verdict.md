## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ subject=clean_subject,` / `+ body=clean_body[:MAX_BODY_CHARS],`: the model reads a scrubbed ticket, but placeholders such as `[card number]` leave what it needs to choose the queue. |
| F2 | broken by a slip | `+ stated = match.group("open") or match.group("sep").strip()`: after "is"/"was" any plain word counts as a password, so "password was stolen" reaches the model as "password was [removed]", losing the urgency cue. |
| F3 | moved toward code | `+ summary = " ".join(_redact(fields.get("summary", ""), secrets).split()) or clean_subject`: a regex override applied to the model's summary. The prompt text "Never put card numbers..." alone would have been criteria. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; the `general` and `normal` defaults stay as they were, so the gap is unchanged. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | moved toward code | `+ ... or clean_subject`: the fallback is no longer the subject as the customer wrote it but a version code has rewritten. One line and the 120 cap are unchanged. |
| C7 | moved toward code | `+ clean_subject = _redact(subject, secrets)` / `+ clean_body = _redact(body, secrets)`: code now removes parts of the ticket beyond the cap the line allows. Still one call, no retry. |
| C8 | held | not touched; `_redact` runs after the `ValueError` check and parsing is unchanged. |
| B1 | held | `+ body=clean_body[:MAX_BODY_CHARS],`: still one call, and the body is still cut to the cap. |

## Trial

- where: both
- flagged: no
- stopped: no