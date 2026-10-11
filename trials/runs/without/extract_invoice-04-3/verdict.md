## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: `[^\d]+$` strips a trailing `EUR` from amount strings only, and the `currency` field is still the model's answer. |
| F4 | held | not touched |
| F5 | moved toward code | `+ text = re.sub(r"^[^\d+\-.,]+|[^\d]+$", "", value.strip())`: a trailing minus or brackets (`"1.250,00-"`, `"(125.00)"`) are stripped, so code turns the model's negative amount into a positive one. Before, these raised. |
| F6 | moved toward code | `+ if len(tail) == 3 and re.fullmatch(r"[1-9]\d{0,2}", head): raise InvoiceError(f"{label} is ambiguous, thousands or decimals: {value!r}")`: a quantity the model gives as `"2.500"` was read as 2.5 and is now refused by a code rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ number = Decimal(_plain_number(value, label))`: more printed forms of an amount are accepted, but the line fixes keys, date format and at least one line, not number format. Errors still name the field. |
| C2 | held | not touched: the gap (only three capital letters checked) is as it was. |
| C3 | held | not touched: the total is still the amount due, with no net or VAT fields. |
| C4 | held | not touched: `"amount": _cents(quantity * unit_price)` is unchanged, and the prompt still asks only for `quantity` and `unit_price`. |
| C5 | held | not touched: `"ok" if lines_total == total else "mismatch"` is unchanged. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, no retry. |
| C7 | held | not touched: the empty-text refusal, the JSON reading and the currency upper-casing are unchanged; `_plain_number` is an added step. |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: both
- flagged: no
- stopped: no
