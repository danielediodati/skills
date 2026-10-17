## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `+ if asked.workout is not None or asked.groups: raise PlanRejected("an adaptation plans today's workout of the mesocycle, so it names no other workout and no groups")` refuses an adaptation for naming another workout. `request = requested(connection, today, asked).request` then fixes the groups to the slot's, which binds the admissible set, and `without` is restricted to declared equipment. |

## Trial

- where: both
- flagged: no
- stopped: no
- asked move: not asked