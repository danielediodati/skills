## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Use null for a field that is not on the invoice or cannot be read.`: the model still decides which text is which field. |
| F2 | held | not touched |
| F3 | held | `+Use null for a field that is not on the invoice or cannot be read.`: a general rule the model applies by reading; it can still infer the currency. |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward the model | `- raise InvoiceError("no invoice lines")` `+ missing.append("lines")` and `+ except InvoiceError: missing.append(name); return None`: a bad shape no longer raises, it returns a record. |
| C2 | held | `+ if not re.fullmatch(r"[A-Z]{3}", currency):` only moved into `_currency`: the gap to ISO 4217 is as it was. |
| C3 | held | not touched |
| C4 | held | `+ amount = _cents(quantity * unit_price)` when both are known, else `None`: still computed by code, never read from the model. |
| C5 | held | `+ status = "ok" if lines_total == total else "mismatch"` unchanged when nothing is missing; `incomplete` is never `ok`. |
| C6 | held | not touched |
| C7 | held | `+ currency = _text(data, "currency").upper()` kept in `_currency`; empty-text refusal and `_load_json` not touched. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: yes
- stopped: no
