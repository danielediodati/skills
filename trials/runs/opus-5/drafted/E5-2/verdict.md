## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `catalog.values(connection, "movement_pattern")` and `catalog.joint_values(connection)` go into the system prompt, but "nothing in the list says which to pick" and `classify` keeps the granularity. Telling the model which names the catalog holds informs its judgement, with no enum in the schema and no closed list to pick from. |

## Trial

- where: plan
- flagged: yes
- stopped: partial
- asked move: not asked