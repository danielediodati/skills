## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | `sign, digits = match.groups()` … `return sign + "".join(groups) + "." + decimals`: the sign is carried through, so negative amounts are still accepted. |
| F6 | moved toward code | `+ if len(tail) == 3 and head != "0" and head != "": raise InvoiceError(f"{error} (ambiguous separator)")`: a quantity the model writes as `"1.250"` (kilos, hours) loaded as 1.25 before and is now refused by a code rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | moved toward code | `+ text = _plain_number(text, ...)` with `# Both kinds present: the last one is the decimal mark.`: a code rule now decides what a written amount means, and refuses numeric strings such as `"1.250"` that the line does not forbid. |
| C2 | held | not touched; the gap (three capital letters only) is left as it was. |
| C3 | held | not touched; the gap (no separate net, VAT and total) is left as it was. |
| C4 | held | not touched: `_cents(quantity * unit_price)` still computes each amount in code. |
| C5 | held | not touched: `lines_total == total` is still compared to the cent, with no tolerance. |
| C6 | held | not touched: still one `model(PROMPT.format(text=text))` call, with no retry or fallback. |
| C7 | held | not touched: the empty-text refusal, the JSON reading and the currency upper-casing are unchanged. |
| B1 | held | not touched: one model call per invoice. |

## Trial

- where: code
- flagged: no
- stopped: no
