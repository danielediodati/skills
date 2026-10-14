## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched: the model still picks the queue from the text it is given. |
| F2 | held | not touched: the prompt's urgency wording is unchanged and the model still judges it. |
| F3 | held | not touched: the model still writes the summary. |
| C1 | held | not touched: `QUEUES` and `_choice(fields.get("queue"), QUEUES, "general")` are unchanged. |
| C2 | held | not touched: `URGENCIES` and `_choice` are unchanged. |
| C3 | held | not touched: the `"general"` and `"normal"` defaults are as before, so the gap is not widened or closed. |
| C4 | held | not touched: the tier is still not in the prompt and the enterprise raise is unchanged. |
| C5 | held | not touched: `RESPOND_WITHIN_HOURS[urgency]` is unchanged. |
| C6 | held | not touched: the summary cleaning, the 120-character cap and the subject fallback are unchanged. |
| C7 | moved toward code | `+ body=_shorten(_without_quoted_text(body), MAX_BODY_CHARS)`: code now drops `>` lines, `wrote:` lines and everything after "Original Message" by regex, then keeps head and tail with the middle left out, where the line says the body is cut to a fixed cap. |
| C8 | held | the empty-ticket `ValueError` check and the `FIELD` parsing are untouched. |
| B1 | held | still one model call; the cap going from 2000 to 4000 is a budget number and does not move the line. |

## Trial

- where: prompt
- flagged: yes
- stopped: no