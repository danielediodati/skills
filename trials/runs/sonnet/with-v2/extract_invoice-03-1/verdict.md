## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: `PROMPT` is unchanged and `_text(data, "supplier")` / `_text(data, "invoice_number")` are the same checks, now wrapped in `read(...)`. |
| F2 | held | not touched: the prompt is unchanged, and `_issue_date` is the old `date.fromisoformat(raw_date)` check moved into a helper. |
| F3 | held | not touched: the model still names the currency, and `_currency` is the old check moved into a helper. |
| F4 | held | not touched: the model still decides which entries are lines; `for number, raw in enumerate(raw_lines, start=1)` keeps every one. |
| F5 | held | not touched: `_number` is unchanged and no sign rule is added. |
| F6 | held | not touched: `_number` is unchanged and no whole-number rule is added. |
| F7 | held | `+ line = {"description": str(raw.get("description") or "").strip()}`: an empty description is still accepted and never listed in `missing`. |
| F8 | held | not touched: the supplier is still taken as written through `_text(data, "supplier")`. |
| C1 | held | `+ raise InvoiceError("; ".join(messages), partial=record, missing=missing)`: any missing or malformed field still raises, and the message names every field. |
| C2 | held | not touched: `_currency` keeps `re.fullmatch(r"[A-Z]{3}", currency)`, so the gap to ISO 4217 is as it was. |
| C3 | held | not touched: there are still no net or VAT fields, so the gap is as it was. |
| C4 | held | `+ line["amount"] = _cents(line["quantity"] * line["unit_price"])`: amounts are still computed by code, and are `None` when a factor is unreadable, never read from the model. |
| C5 | held | `+ record["status"] = "ok" if lines_total == record["total"] else "mismatch"`: exact comparison with no tolerance, and a partial record gets no `status`. |
| C6 | held | not touched: `data = _load_json(model(PROMPT.format(text=text)))` is still the only call, with no retry or fallback value. |
| C7 | held | not touched: the empty-text refusal and `_load_json` are unchanged, and `_currency` keeps `.upper()`. |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: code
- flagged: yes
- stopped: partial
