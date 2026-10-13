## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | moved toward code | `+ if match[2] == "." or date_order == "DMY":` and `+ candidates = _date_readings(raw_date, date_order)`: code and a caller argument now decide what an ambiguous date means; the prompt tells the model `do not reformat or convert it`. |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward code | `- "issue_date" (YYYY-MM-DD)` replaced by `"issue_date_text"`, plus the new rule `+ if _squash(raw_date) not in _squash(text):`; code now builds the date itself and fixes the answer more tightly than the line says. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT fields) is left as it was. |
| C4 | held | not touched |
| C5 | held | `+ "status": ("mismatch" if lines_total != total`: lines that do not add up to the total still give `mismatch`, with no tolerance; `ambiguous_date` only applies when they do add up. |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call, with no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no