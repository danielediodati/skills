## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = _resolve_owner(fields[1], by_name)` with `+ return len(short) >= 3 and long_.startswith(short)`: a code rule now maps the model's text to an attendee, and `+ return fits[0] if len(fits) == 1 else None` still sets anyone else to `None`. The prompt also fixes the form: `+ written with the full name from the list above even if the notes use a first name or nickname`. |
| F4 | held | not touched |
| C1 | held | not touched: an owner that resolves to nobody still gives `None` and the item stays. |
| C2 | held | not touched |
| C3 | held | not touched: the gap stays as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `MAX_ITEMS = 10` stays, so the gap is as it was. |
| C6 | held | not touched: `if (_key(task), owner) in seen` is unchanged and now compares the resolved owner. |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched: still one `model(prompt)` call. |

## Trial

- where: both
- flagged: no
- stopped: no
