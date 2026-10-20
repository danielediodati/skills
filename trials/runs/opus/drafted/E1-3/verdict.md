## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | moved toward code | `plan.adaptation_requested` builds the request with `requested(..., replace(asked, workout=found.slot, groups=()))`, so the adaptation is bound to the slot's groups, the declared equipment and the cap. The emit schema and `validate` enforce this, and the new test asserts `list(request.groups) == ["legs"], "checked against today's slot"`. |

## Trial

- where: both
- flagged: yes
- stopped: no
- asked move: not asked