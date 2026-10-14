## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | moved toward code | `+ elif date_order == "DMY": day, month = first, second` / `+ raise InvoiceError("issue_date is ambiguous ...")`: code now fixes the day/month reading, and the prompt asks for `issue_date_as_printed` instead of the model's own reading of `YYYY-MM-DD`. |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ issue_date = _issue_date(_text(data, "issue_date_as_printed"), date_order)`: the key is renamed, but code still validates it and raises `InvoiceError` naming the field. |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched; still one `model(PROMPT.format(text=text))` call. |
| C7 | held | empty-text check, fence-tolerant JSON reading and currency `.upper()` unchanged; `+ if date_order not in DATE_ORDERS: raise ValueError` is checked before the model is called. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no