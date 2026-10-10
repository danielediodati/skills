## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Use null for a field that is not on the invoice or cannot be read.` lets the model report absence; which text is which field is still its reading. |
| F2 | held | not touched: an ambiguous date is still the model's to resolve, and `_date` only parses the `YYYY-MM-DD` it answers. |
| F3 | moved toward code | `+Use null for a field that is not on the invoice or cannot be read.`: with no currency stated, the prompt dictates `null` where the line leaves inferring it to the model. |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched: `"description": str(raw.get("description") or "").strip()` is unchanged and an empty description is not added to `missing`. |
| F8 | held | not touched |
| C1 | moved toward the model | `- raise InvoiceError("no invoice lines")` / `+ missing.append("lines")`, and `field()` catches `InvoiceError`: a malformed answer now returns a record where the line says it raises. |
| C2 | held | The gap is unchanged: `+ if not re.fullmatch(r"[A-Z]{3}", currency):` is the same three-letter check moved into `_currency`, with no ISO 4217 list. |
| C3 | held | not touched |
| C4 | held | `+ amount = _cents(quantity * unit_price)`: still computed by code, `None` when a factor is unknown, never read from the model. |
| C5 | moved toward the model | `+ if missing:` / `+ status = "incomplete"` overrides the comparison: a total that differs from the lines is no longer reported as `mismatch` (`test_incomplete_wins_over_mismatch`). |
| C6 | held | not touched: still the single `data = _load_json(model(PROMPT.format(text=text)))`, with no retry. |
| C7 | held | Empty-text refusal and `_load_json` are unchanged; `+ currency = _text(data, "currency").upper()` keeps the upper-casing in `_currency`. |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: yes
- stopped: no
