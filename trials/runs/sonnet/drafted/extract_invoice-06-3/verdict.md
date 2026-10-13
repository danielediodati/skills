## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ That is one invoice line: report it with quantity 1 and that amount as its unit_price.`: a general rule on how to report a single-amount charge; the model still reads each invoice to decide which entries are such charges. |
| F5 | held | not touched |
| F6 | held | not touched; `quantity 1` applies only to charges printed with no quantity, and code adds no whole-number rule. |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | not touched in code: a line with no quantity still raises `line N quantity is missing`; the change is only `+ report it with quantity 1 and that amount as its unit_price` in the prompt. |
| C2 | held | not touched; the gap (three capital letters only) is left as it was. |
| C3 | held | not touched; the gap (total is the amount due, no net or VAT fields) is left as it was. |
| C4 | held | `+ report it with quantity 1 and that amount as its unit_price`: the amount is still `_cents(quantity * unit_price)` computed by code, not read from the model. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: no
- stopped: no