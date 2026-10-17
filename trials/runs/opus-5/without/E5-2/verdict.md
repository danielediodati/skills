## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | `+ **The exclusion vocabulary in the brief, read from the catalog**: catalog.values(connection, "movement_pattern") and catalog.joint_values(connection)`: this tells the model which names the catalog holds, and `classify` still checks the name afterwards. `+ A bounded refusal loop ... with the refusal as a message naming it` sends a refusal back for the model to read. The ticket proposes no enum in the schema. |

## Trial

- where: plan
- flagged: no
- stopped: no
- asked move: not asked