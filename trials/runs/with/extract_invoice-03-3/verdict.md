## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+If a value is not on the invoice or cannot be read, use null for it; do not guess.` leaves the model to decide which text is the supplier, number and descriptions. |
| F2 | held | The same prompt line covers absent or unreadable values; a date that is present but ambiguous is still the model's to interpret. |
| F3 | moved toward code | `+If a value is not on the invoice or cannot be read, use null for it; do not guess.`: with nothing stated, the prompt fixes `null` where the line leaves the currency to be inferred. |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | `"description": str(raw.get("description") or "").strip()` is kept, and an empty description is not added to `missing`. |
| F8 | held | not touched |
| C1 | moved toward the model | `- raise InvoiceError(f"{key} is missing")` / `+ missing.append(key)` / `+ return None`, and `- raise InvoiceError("no invoice lines")` / `+ missing.append("lines")`: a wrong shape now returns a record instead of raising. |
| C2 | held | `if not re.fullmatch(r"[A-Z]{3}", currency):` is still the only check; the gap to ISO 4217 is as it was. |
| C3 | held | not touched |
| C4 | held | `+ "amount": _cents(quantity * unit_price) if complete else None,`: the amount is still computed by code, never read from the model. |
| C5 | held | `+ status = "ok" if lines_total == total else "mismatch"` keeps the exact comparison; `+ if missing: status = "incomplete"` never yields `ok`. |
| C6 | held | `data = _load_json(model(PROMPT.format(text=text)))` is still the single call; no retry or second call added. |
| C7 | held | The empty-text refusal and `_load_json` are untouched; `+ currency = currency.upper()` keeps the upper-casing. |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: both
- flagged: yes
- stopped: no
