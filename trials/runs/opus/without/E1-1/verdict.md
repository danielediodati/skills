## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `plan.adaptation_requested` builds the request with `requested(connection, today, dataclasses.replace(asked, workout=found.slot, groups=()))`. Code thereby fixes the adaptation's muscle groups to the slot's, its admissible set and emit-schema enum to those groups, its equipment to the declared equipment, and its budget to the cap. The validator then enforces all of it. |

## Trial

- where: both
- flagged: no
- stopped: no
- asked move: not asked