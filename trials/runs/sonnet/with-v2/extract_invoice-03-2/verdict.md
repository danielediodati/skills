## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched; `_date` is the old ISO check moved into a helper, with the prompt unchanged. |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched; `"description": str(raw.get("description") or "").strip()` is kept and an empty description is still not a problem. |
| F8 | held | not touched |
| C1 | held | `+ if problems: raise InvoiceError("; ".join(message for _, message in problems), problems=[...], partial=partial)`: every shape failure still raises, naming the fields; nothing unchecked is returned. |
| C2 | held | `+ if not re.fullmatch(r"[A-Z]{3}", currency):` in `_currency` is the same three-letter check moved; the gap is left as it was. |
| C3 | held | not touched; the total is still the amount due and the gap is left as it was. |
| C4 | held | `+ "amount": (_cents(quantity * unit_price) if quantity is not None and unit_price is not None else None)`: still computed by code, and `None` appears only in the raised `partial`. |
| C5 | held | not touched; `"status": "ok" if lines_total == total else "mismatch"` is unchanged and reached only when there are no problems. |
| C6 | held | not touched; `data = _load_json(model(PROMPT.format(text=text)))` is still the single call, with no retry or fallback. |
| C7 | held | not touched; the empty-text refusal and `_load_json` are unchanged, and `.upper()` is kept in `_currency`. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: yes
- stopped: partial
