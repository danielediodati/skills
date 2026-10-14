## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | moved toward code | `+ if date_order == "DMY": return _make_date(year, second, first, raw)`: a code-side `date_orders` table keyed on supplier now fixes day/month, and the prompt says "copy it, do not reformat or reorder its parts", so the model no longer interprets the date. |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched; the supplier name is still read as written and is only used as a lookup key for date order. |
| C1 | moved toward the model | `- date.fromisoformat(raw_date)` replaced by `_issue_date` accepting `05/08/2026`, `5 August 2026`, `Aug 5, 2026` and unpadded ISO: `issue_date` is no longer required to arrive as `YYYY-MM-DD`. |
| C2 | held | not touched; still only checks three capital letters, so the gap is as before. |
| C3 | held | not touched; the gap is as before. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched; still one `model(...)` call. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no