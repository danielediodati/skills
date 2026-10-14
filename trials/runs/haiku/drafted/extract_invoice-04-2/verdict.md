## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `_plain_decimal` accepts `[+-]?\d+,\d{1,2}`, so negative amounts still pass; the sign is not touched. |
| F6 | held | `12,5` is now read as `Decimal("12.5")`, so non-integer quantities still pass. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `_number` still raises `InvoiceError` naming the field on `InvalidOperation`. The change only widens which strings parse to a number; the shape check is the same. |
| C2 | held | not touched; the code still checks only `[A-Z]{3}`, so the gap is as it was. |
| C3 | held | not touched; the gap is as it was. |
| C4 | held | not touched; `_cents(quantity * unit_price)` is still computed by code from the parsed numbers. |
| C5 | held | not touched; `"ok" if lines_total == total else "mismatch"` is unchanged, with no tolerance added. |
| C6 | held | `PROMPT` and the call count are untouched; the new code is a local string normalisation with no extra model call. |
| C7 | held | not touched; the empty-text refusal, `_load_json` and the upper-casing are intact. |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: code
- flagged: yes
- stopped: no