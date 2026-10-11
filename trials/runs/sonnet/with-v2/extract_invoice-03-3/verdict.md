## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched: `_date` is the same `date.fromisoformat` check on the model's answer, and the prompt is unchanged. |
| F3 | held | not touched: `_currency` keeps the same check, and the model still infers the currency. |
| F4 | held | not touched |
| F5 | held | not touched: `_number` is unchanged and still accepts negative amounts. |
| F6 | held | not touched: `_number` is unchanged and still accepts non-integer quantities. |
| F7 | held | `"description": str(raw.get("description") or "").strip()` is kept as it was: an empty description is still accepted and is not listed as a problem. |
| F8 | held | not touched |
| C1 | held | `+ raise InvoiceError("; ".join(problems.values()), missing=problems, partial=partial, unreadable=unreadable)`: every shape failure still raises, with messages naming the fields. No partial record is returned. |
| C2 | held | `+ if not re.fullmatch(r"[A-Z]{3}", currency):` is the same three-letter check moved into `_currency`. The gap is left as it was. |
| C3 | held | not touched: the gap is left as it was. |
| C4 | held | `+ if quantity is not None and unit_price is not None: amount = _cents(quantity * unit_price)`: amounts are still computed by code, and are `None` when a factor is unreadable. |
| C5 | held | not touched: `"status": "ok" if lines_total == total else "mismatch"` is only reached when there are no problems. |
| C6 | held | not touched: still a single `model(PROMPT.format(text=text))`, with no retry or fallback. |
| C7 | held | `+ currency = raw.strip().upper()`: upper-casing moved into `_currency`. The empty-text refusal and `_load_json` are unchanged. |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: code
- flagged: yes
- stopped: partial
