## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | `+ Decide which from what the invoice itself shows: the supplier's country and address, the currency, the language...`: criteria that inform the model's reading; no day-month rule is fixed and the model still decides each date. |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | `+ If nothing on the invoice settles it, do not guess: set "issue_date" to null.`: the unchanged `_text` check still raises `InvoiceError` naming the field ("issue_date is missing"), so nothing unchecked reaches the ledger. |
| C2 | held | not touched; the gap (only three capital letters checked) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net/VAT fields) is left as it was. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched; the null date raises an error, with no retry, second call or fallback date added. |
| C7 | held | not touched |
| B1 | held | not touched; still one model call per invoice. |

## Trial

- where: prompt
- flagged: yes
- stopped: partial