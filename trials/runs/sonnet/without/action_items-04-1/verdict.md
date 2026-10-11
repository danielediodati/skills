## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | moved toward code | `+ owner = _resolve_owner(fields[1], by_name)` with `+ return len(short) >= 3 and long_.startswith(short)` and `+ return fits[0] if len(fits) == 1 else None`: a prefix-matching rule now decides which attendee a short name means and overrides the model's text. Non-attendees and several owners still become `None`, and the prompt still demands "the full name from the list above". |
| F4 | held | not touched |
| C1 | held | not touched: an item whose owner resolves to `None` is still appended. |
| C2 | held | not touched |
| C3 | held | not touched: the gap is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched: `MAX_ITEMS = 10` is left as it was. |
| C6 | held | not touched: `if (_key(task), owner) in seen` is unchanged and still a string comparison in code, now on the resolved owner. |
| C7 | held | not touched |
| C8 | held | not touched: still one `model(prompt)` call, with the same parsing and skipping. |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no
