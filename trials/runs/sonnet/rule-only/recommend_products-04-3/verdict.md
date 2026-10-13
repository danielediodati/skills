## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched: a pick whose reason fails the check stays in the strip, only `pick["reason"] = ""` changes. |
| F4 | moved toward code | `+ if not (_numbers_agree(pick["reason"], pick) and _standing_agrees(pick["reason"], pick, picks)): pick["reason"] = ""`: keyword and number rules check the claims and override the model's reason, where the line says claims are not checked. |
| F5 | held | The prompt and code do not set the language; the added `BOUND`, `TOP_RATED` and `CHEAPEST` patterns are English keywords but fix no language for the reason. |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | not touched: `" ".join(reason.split())[:MAX_REASON_CHARS]` is unchanged, and a blanked reason keeps its product. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: yes
- stopped: no
