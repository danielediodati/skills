## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Only include a product if it is the kind of thing the customer is looking for.` and `+If nothing in the list suits the search (...), answer with exactly: NONE`: criteria the model still applies by reading each search; no code or keyword decides. |
| F2 | held | not touched: "best first" stays in the prompt and code keeps the model's order. |
| F3 | held | `+Do not pad the answer: ... fewer than {limit} picks is fine` and `answer with exactly: NONE`: the model still chooses from none to `limit`, as the line says. |
| F4 | held | `+one short reason that says why it suits this search, addressed to the customer`: informs what a good reason is; the wording stays the model's and is not checked. |
| F5 | held | not touched: "addressed to the customer" is kept and no language is fixed. |
| C1 | held | not touched: the prompt still lists every in-stock product, with no pre-filter. |
| C2 | held | not touched: the id check, dedupe and `limit` cut are unchanged; `NONE` is not a valid id and is dropped. |
| C3 | held | not touched |
| C4 | held | not touched in code: a `NONE` answer gives `[]` through the existing parse (`self.assertEqual(recommend("NONE", query="kettle"), [])`), with no fallback list added. |
| C5 | held | not touched |
| C6 | held | not touched: still a single `model(...)` call, no retry. |
| C7 | held | not touched: `NONE` is skipped by the existing rule for lines that are not valid ids. |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: no
- stopped: no