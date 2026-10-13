## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | `+ - urgent: something is broken for the customer or their users right now (...)` and `+ A deadline or a firm tone alone does not make a ticket urgent.`: criteria in the prompt, where the line says they go; the model still reads each ticket and picks the level. |
| F3 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched: the added prompt text defines the same four levels, and `URGENCIES` and `_choice` are unchanged. |
| C3 | held | not touched: the `general` and `normal` defaults remain as before, so the gap is neither closed nor widened. |
| C4 | held | Seam code not touched: the tier is still not in the prompt and the one-level raise in code is unchanged; the added test `+ self.assertNotIn("enterprise", model.prompts[0].lower())` only asserts it. |
| C5 | held | not touched |
| C6 | held | not touched |
| C7 | held | not touched: still one call, body cut at `MAX_BODY_CHARS`. |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial