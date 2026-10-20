# E3 - How many cycles a mesocycle lasts, as a constant

| from | to | seam | direction | model | lived in | strength |
|---|---|---|---|---|---|---|
| `8f4eeae` | `039f470` | planner, mesocycle | toward code (substitution) | Opus 5 | a recommendation, same day | weak |

## The line

Who decides how many cycles a mesocycle lasts. The mesocycle did not exist yet: the grilling below produced ADR-0008.

- **Before**: no line. TRAINER.md had mesocycles only as the boundary for progression and the supervisor; the planner planned one workout at a time.
- **The agent's recommendation**: a declaration in `training.toml`, `cycles_per_scheda = 4`, which the bot follows as given, against letting the bot choose between 4 and 5 with a reason. Its argument: it is the user's rhythm, and the bot has no methodology to derive it from yet.

## The commits

| commit | date | what |
|---|---|---|
| none | 2026-09-21 | The recommendation, in the grilling. |
| `039f470` Withdraw ticket 9.4 for the mesocycle | 2026-09-21 | ADR-0008: "a number of cycles the agent chooses with a reason (no fixed range)". |

## Declared?

The recommendation was explicit, and the user turned it down.

## The user's correction

2026-09-21, paraphrased: the bot chooses, with a reason, and not between 4 and 5.

## Why it is weak for a replay

The drift sits in a design still being made: no charter at the parent could state a line that did not exist.
