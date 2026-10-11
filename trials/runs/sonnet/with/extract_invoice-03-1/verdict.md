## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `- raise InvoiceError("no invoice lines")` / `+ problems.append({"field": "lines", "reason": "no invoice lines"})` and `+ return None` in `attempt`: a missing key, a bad date or no lines no longer raises `InvoiceError`, where the line says anything else raises. |
| C2 | held | not touched: `_currency` still checks only `[A-Z]{3}`, so the gap is as it was. |
| C3 | held | not touched |
| C4 | held | `+ amount = _cents(quantity * unit_price)`: still computed by code, and `None` when an operand is unreadable, never read from the model. |
| C5 | held | `+ status = "ok" if lines_total == total else "mismatch"`: same exact comparison when there are no problems; with problems the status is `incomplete`, never `ok`. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, with no retry and no second call. |
| C7 | held | `+ currency = _text(data, "currency").upper()` moved into `_currency` unchanged; the empty-text refusal and `_load_json` are not touched. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
