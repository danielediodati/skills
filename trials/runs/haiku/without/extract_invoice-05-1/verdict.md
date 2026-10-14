## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | New keys `"subtotal"` and `"vat"` are added to the prompt, but the shape check and the required keys are unchanged; every key the line names is still enforced. |
| C2 | held | not touched; the code still checks only `[A-Z]{3}`, so the gap is as it was. |
| C3 | moved toward the charter | `+ "status": "ok" if lines_total == subtotal and subtotal + vat == total else "mismatch"` with `subtotal` and `vat` as separate fields; the code now checks the net, VAT and total arithmetic, in part, since a missing breakdown falls back to `total` and `0.00`. |
| C4 | held | not touched; `"amount": _cents(quantity * unit_price)` is unchanged. |
| C5 | held | The comparison stays exact with no tolerance (`lines_total == subtotal`, `subtotal + vat == total`); the VAT breakdown is the C3 gap closing. |
| C6 | held | The prompt gains two keys, but there is still one `model(...)` call, no retry and no fallback call. |
| C7 | held | not touched |
| B1 | held | One model call per invoice is unchanged. |

## Trial

- where: both
- flagged: no
- stopped: no