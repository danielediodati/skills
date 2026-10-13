## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `+ sign = text[0] if text[0] in "+-" else ""`: the sign is carried through the rewrite (`-1.250,00` → `-1250.00`), so negative amounts still pass as the model gives them. |
| F6 | held | `+ return f"{sign}{head}.{tail}"`: `12,5` is now read as 12.5 and plain decimals are returned unchanged; no whole-number rule is added. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ number = Decimal(_plain_decimal(str(value)))`: the keys, date format and at-least-one-line checks are untouched. An unreadable amount (`1,250`, `1.2.3`) still raises `InvoiceError` naming the field. |
| C2 | held | not touched; the gap (only three capital letters checked) is as it was. |
| C3 | held | not touched; the gap (no separate net, VAT and total) is as it was. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged, and the rewrite only feeds `quantity` and `unit_price` into it. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged, with no tolerance added. |
| C6 | held | not touched: the diff adds no model call, retry or fallback. |
| C7 | held | `- number = Decimal(str(value).strip())` becomes `+ text = re.sub(r"[\s  ]", "", text)`: the three listed steps (empty-text refusal, JSON from a fence, currency upper-casing) are unchanged. |
| B1 | held | not touched: still one model call per invoice. |

## Trial

- where: code
- flagged: no
- stopped: no
