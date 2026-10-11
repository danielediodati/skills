## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | `+ line["description"] = str(raw.get("description") or "").strip()`: an empty description is still accepted and never listed in `problems`. |
| F8 | held | not touched |
| C1 | moved toward the model | `- raise InvoiceError(f"issue_date is not a date: {raw_date!r}")`, `- raise InvoiceError("no invoice lines")` replaced by `+ problems.append(...)` / `+ return None`: an answer of the wrong shape now returns a record with `status = "incomplete"` where the line says it raises. |
| C2 | held | `+ if not re.fullmatch(r"[A-Z]{3}", code):`: still only three capital letters; the gap is left as it was. |
| C3 | held | not touched |
| C4 | held | `+ line["amount"] = _cents(line["quantity"] * line["unit_price"])`: still computed by code, `None` when a factor is unreadable, never read from the model. |
| C5 | held | `+ status = "ok" if lines_total == total else "mismatch"`: exact comparison kept. `+ if problems: status = "incomplete"` comes first, but such a record still goes to a clerk. |
| C6 | held | not touched |
| C7 | held | `+ code = _text(value).upper()`: upper-casing kept; the empty-text refusal and `_load_json` are not touched. |
| B1 | held | not touched |

## Trial

- where: code
- flagged: no
- stopped: no
