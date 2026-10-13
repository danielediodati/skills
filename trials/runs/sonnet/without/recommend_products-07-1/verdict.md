## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ Only pick a product if it is what the customer is looking for or a close substitute for it.`: a criterion the model still applies by reading each search; no rule or filter in code fixes the picks. |
| F2 | held | `+ ...that genuinely suit the search, best first.`: order is still the model's; code keeps the answer's order. |
| F3 | held | `+ Fewer is fine.` and `+ answer with the single word NONE`, with `+ if lines and lines[0].rstrip(".!").upper() == "NONE": return []`: code honours the model's own "none", it sets no count or threshold. |
| F4 | held | `+ customer, saying why it suits their search`: restates the charter's own description of a good reason; the wording stays the model's and is not checked. |
| F5 | held | Not touched: "addressed to the customer" is kept and no language is fixed. |
| C1 | held | Not touched: the prompt still lists every in-stock product, with no pre-filter. |
| C2 | held | `- for line in answer.splitlines():` / `+ for line in lines:`: the same lines minus blanks; the id, repeat and `limit` checks are unchanged. |
| C3 | held | Not touched. |
| C4 | held | `+ return []` on `NONE`: an empty strip with no fallback list; an answer with no valid id still gives `[]`. |
| C5 | held | Not touched. |
| C6 | held | Not touched: still a single `model(...)` call, no retry. |
| C7 | held | `+ lines = [line.strip() for line in answer.splitlines() if line.strip()]`: blank lines dropped, markers and chatter still skipped by the unchanged loop; the guards are untouched. |
| B1 | held | Not touched: one model call per search. |

## Trial

- where: both
- flagged: no
- stopped: no