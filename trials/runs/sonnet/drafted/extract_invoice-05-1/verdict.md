## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+Every row of the invoice that adds to or subtracts from the amount due is a line:` / `+items, delivery, discounts (negative unit_price) and tax rows such as VAT`: the prompt fixes which classes of entry are lines, so the model can no longer leave a tax row out. |
| F5 | held | `+discounts (negative unit_price)` tells the model how to write a discount; negative amounts are still accepted by code as before. |
| F6 | held | `+(quantity 1, unit_price the tax amount as printed)` concerns tax rows only; code still accepts any finite quantity. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | not touched; the keys and the shape checks are unchanged. |
| C2 | held | not touched; the gap (three capital letters only) is as it was. |
| C3 | held | Gap left as it was: no net or VAT field is added, and `+tax rows such as VAT (quantity 1, unit_price the tax amount as printed)` folds VAT into the lines instead. |
| C4 | held | Amounts are still computed by code; `+do not compute or correct any figure` asks the model for no arithmetic. |
| C5 | held | not touched; the exact comparison `lines_total == total` is unchanged. |
| C6 | held | not touched; still one call with no retry or fallback. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: prompt
- flagged: no
- stopped: no