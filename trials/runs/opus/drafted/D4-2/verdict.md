## Lines

| line | verdict | reason |
| --- | --- | --- |
| C1 | held | `- (SHORTER, f"Solo {SHORTER_MINUTES} minuti"),` and `- if tap.action == SHORTER: return planner.refused(..., minutes=SHORTER_MINUTES)`: only the third button and its 30-minute budget are gone. The answers stay fixed buttons answered through `Negotiation.answer` by proposal id, and the entrance still does not read text as an answer to a waiting plan. |

## Trial

- where: code
- flagged: yes
- stopped: partial
- asked move: not made