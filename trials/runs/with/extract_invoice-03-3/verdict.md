## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ If a value is not on the invoice or cannot be read, use null for it; do not guess.`: the model still decides which text is which field. |
| F2 | held | Same prompt line: an ambiguous date is on the invoice and readable, so the model still decides what it means. |
| F3 | moved toward code | `+ If a value is not on the invoice or cannot be read, use null for it; do not guess.`: with no currency stated the prompt fixes `null`, where the line leaves inferring it to the model. |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched: `"description": str(raw.get("description") or "").strip()` is kept and an empty description is not added to `missing`. |
| F8 | held | not touched |
| C1 | moved toward the model | `- raise InvoiceError(f"{key} is missing")` `+ missing.append(key)` `+ return None`, and `- raise InvoiceError("no invoice lines")` `+ missing.append("lines")`: a wrong shape now returns a record instead of raising. |
| C2 | held | Gap left as it was: `re.fullmatch(r"[A-Z]{3}", currency)` is still the only check on the code. |
| C3 | held | not touched |
| C4 | held | `+ "amount": _cents(quantity * unit_price) if complete else None`: the amount is still computed by code, never read from the model. |
| C5 | held | `+ status = "ok" if lines_total == total else "mismatch"` is reached only when `missing` is empty: `ok` still needs equality to the cent. |
| C6 | held | not touched: still the single `model(PROMPT.format(text=text))` call, with no retry. |
| C7 | held | Empty-text refusal and `_load_json` are not touched; `+ currency = currency.upper()` keeps the upper-casing. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: yes
- stopped: no
