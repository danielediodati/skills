## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | moved toward code | `+ if states_other_price(reason, product["price"]):` / `+ reason = ""`: code checks a claim in the reason and overrides the model's text, where the line says claims are not checked. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | held | `+ reason = " ".join(reason.split())[:MAX_REASON_CHARS]`: same one-line join and 80-character cut, only moved up; a blanked reason is still kept with its product. |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: code
- flagged: yes
- stopped: no
