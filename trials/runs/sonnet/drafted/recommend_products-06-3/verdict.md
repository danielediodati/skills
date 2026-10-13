## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ if you cannot give a reason, leave it out`: a criterion that informs the choice; the model still reads each product and decides which suit the search. |
| F2 | held | not touched |
| F3 | held | `+ if you cannot give a reason, leave it out`: the model still decides how many, from none to `limit`; no count is fixed by code or prompt. |
| F4 | held | `+ If a product is only a partial fit, say what it offers this search`: restates what a good reason is; the wording stays the model's and is not checked. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+ Every line needs its reason` is only a request in the prompt; the code still cuts to 80 characters and still keeps a pick with an empty reason. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial