## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | not touched |
| F4 | held | `+ Each reason must be a single complete sentence of at most {max_chars} characters.` sets the form of the reason; the model still decides what it says. |
| F5 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched |
| C4 | held | not touched |
| C5 | moved toward code | `- " ".join(reason.split())[:MAX_REASON_CHARS]` → `+ _whole_sentences(...)`: code now cuts back to sentence ends and returns `""` when none fit, which is tighter than "cut to 80 characters". |
| C6 | held | not touched |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no