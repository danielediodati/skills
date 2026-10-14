## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `[+-]?\d+(\.\d+)?...` in `_plain_digits` still lets a negative amount through; the model still decides the sign. |
| F6 | held | `"0,5"` now reads as 0.5 and `Decimal(text)` keeps non-integers; no whole-number rule was added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | Keys, `issue_date` format and the at-least-one-line check are not touched; amounts must still parse as numbers or `InvoiceError` is raised. |
| C2 | held | not touched; the check is still three capital letters, so the gap is as it was. |
| C3 | held | not touched; the total is still compared with the lines, so the gap is as it was. |
| C4 | held | `"amount": _cents(quantity * unit_price)` is not touched; code still computes amounts. |
| C5 | held | `"ok" if lines_total == total else "mismatch"` is not touched; no tolerance added. |
| C6 | held | The prompt change adds an instruction but no call, retry or fallback. |
| C7 | held | `_load_json`, the empty-text check and `.upper()` are not touched. |
| B1 | held | Still one `model(PROMPT.format(text=text))` call. |

## Trial

- where: both
- flagged: no
- stopped: no