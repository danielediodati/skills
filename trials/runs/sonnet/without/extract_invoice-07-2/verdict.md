## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | moved toward code | `+ candidates = _date_candidates(raw_date)` and `+ issue_date = candidates[0 if date_order == "DMY" else 1]`, else `None`: code parses the date and settles ambiguity by a fixed day-month rule or by refusing; the model only copies the text "exactly as printed". |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `- "issue_date" (YYYY-MM-DD)` and `- issue_date = date.fromisoformat(raw_date)` replaced by `+ "issue_date_text" (the issue date copied exactly as printed...)`: the `YYYY-MM-DD` check is removed on purpose, so free-form date text now passes. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT) is left as it was. |
| C4 | held | not touched |
| C5 | held | `+ "status": ("mismatch" if lines_total != total else "date_ambiguous" if issue_date is None else "ok")`: the comparison is still exact to the cent and a mismatch still takes precedence. |
| C6 | held | not touched; still a single `model(PROMPT.format(text=text))` call, with no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no