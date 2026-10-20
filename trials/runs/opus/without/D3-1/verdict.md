## Lines

| line | verdict | reason |
| --- | --- | --- |
| C1 | moved toward the model | `+ request = dataclasses.replace(request, groups=(), allocation=(), adapting=...)`: the request no longer carries the slot's muscle groups, so `every_group_trained` and the admissible-by-group check no longer bind the plan; the prompt now says "What they said comes first: it decides what this workout trains". |

## Trial

- where: both
- flagged: yes
- stopped: no
- asked move: made