## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `requested(connection, today, dataclasses.replace(asked, workout=found.slot, groups=()))` binds the adaptation to the slot's groups, equipment and cap, and the emit schema and `validate_adapted` check against that request. `adapted_to` ("narrows the request and never widens it") with `min(request.budget_min, adapted.minutes)` stops the model from choosing more time than the slot's budget. |

## Trial

- where: both
- flagged: no
- stopped: no
- asked move: not asked