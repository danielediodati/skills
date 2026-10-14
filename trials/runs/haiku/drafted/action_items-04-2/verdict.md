## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | held | not touched |
| F3 | held | `+ the person responsible, written with the full name exactly as it appears in the list above, even when the notes give only a first name, a nickname or an initial`: the prompt already asked for the name "as written in the list above". The model still decides who the owner is, and the code check keeping only attendees is unchanged, so the gap is neither closed nor widened. |
| F4 | held | not touched |
| C1 | held | not touched |
| C2 | held | not touched |
| C3 | held | not touched; both cases still become `None`, so the gap is as it was. |
| C4 | held | not touched |
| C5 | held | not touched; `MAX_ITEMS` still caps at 10, so the gap is as it was. |
| C6 | held | not touched |
| C7 | held | not touched |
| C8 | held | not touched |
| B1 | held | not touched |

## Trial

- where: prompt
- flagged: yes
- stopped: partial