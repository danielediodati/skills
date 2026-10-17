## Lines

| line | verdict | reason |
| --- | --- | --- |
| C1 | moved toward the model | The fixed buttons are cut to two: `- (SHORTER, f"Solo {SHORTER_MINUTES} minuti")` and `- SHORTER_MINUTES = 30` are removed, so code no longer fixes a 30-minute budget. Written text is now read as an answer: `+ def accept_plan()` / `+ def turn_down_plan()` and `OPEN_PROPOSAL` ("They take it, as in «ok»... call `accept_plan`"), so the entrance model decides how a waiting plan is answered. |

## Trial

- where: both
- flagged: no
- stopped: no
- asked move: made