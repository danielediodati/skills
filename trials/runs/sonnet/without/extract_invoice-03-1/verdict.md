## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched: `"description": str(raw.get("description") or "").strip()` is unchanged and still raises no problem. |
| F8 | held | not touched |
| C1 | moved toward the model | `- raise InvoiceError("no invoice lines")` / `+ problems.append({"field": "lines", "reason": "no invoice lines"})` and `+ except InvoiceError as error: problems.append(...)`, `+ return None`: a missing key, bad date or empty lines now returns a record instead of raising. |
| C2 | held | Gap left as it was: `+ if not re.fullmatch(r"[A-Z]{3}", currency):` is the same three-letter check, only moved into `_currency`. |
| C3 | held | not touched: the gap stays as it was, with no net or VAT fields added. |
| C4 | held | `+ "amount": _cents(quantity * unit_price) if known else None`: the amount is still computed by code or left `None`, never read from the model. |
| C5 | held | `+ status = "ok" if lines_total == total else "mismatch"` is the same exact comparison, reached only when `problems` is empty. `+ if problems: status = "incomplete"` can never yield `ok`. |
| C6 | held | not touched: `data = _load_json(model(PROMPT.format(text=text)))` is still the only call, with no retry added. |
| C7 | held | Empty-text refusal and `_load_json` are not touched; `+ currency = _text(data, "currency").upper()` keeps the upper-casing in `_currency`. |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: code
- flagged: no
- stopped: no
