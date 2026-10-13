## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | moved toward code | `+ pairs = {"DMY": [(first, second)], "MDY": [(second, first)],` and `+ date_order = "DMY"  # dotted dates are day-first by convention`: code rules and a caller constant decide the ambiguous date. The model's reading is discarded ("The model's own YYYY-MM-DD is not trusted"). |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward code | `+ printed = _text(data, "issue_date_as_printed")` and `+ raise InvoiceError(f"issue_date_as_printed is not in the invoice: {printed!r}")`: a new required key, a verbatim rule and code-parsable formats fix the shape more tightly than the line. The `- issue_date = date.fromisoformat(raw_date)` check is dropped, but that value is no longer used. |
| C2 | held | not touched; the gap (three capital letters only) is left as it was. |
| C3 | held | not touched; the gap (total as amount due, no net/VAT) is left as it was. |
| C4 | held | not touched |
| C5 | held | `+ if lines_total != total:` / `+ status = "mismatch"`: the exact comparison is kept and takes precedence over the new `date_ambiguous` status. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry or fallback. |
| C7 | held | not touched: the added `date_order` check raises before the model too, and the empty-text refusal, fence reading and upper-casing are unchanged. |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no