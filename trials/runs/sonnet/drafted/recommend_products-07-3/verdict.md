## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+Only pick a product if it is something the customer could reasonably be looking for`: a criterion the model applies by reading each search; no keyword, list or rule fixes its answer. |
| F2 | held | `+Do not pick a product just because it is popular, cheap or well rated.` agrees with the line; "best first" is kept and the model still sets the order. |
| F3 | held | `+If nothing in the list suits the search, answer with nothing at all.` states the "none" end the line already allows; the model still chooses the count, with no threshold in code. |
| F4 | held | not touched |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched in code; the added test `self.assertEqual(recommend_products("kettle", CATALOG, model), [])` only confirms an empty answer gives an empty list, with no fallback. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: no
- stopped: no