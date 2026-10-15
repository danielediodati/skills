# D1 - The admissible set narrowed to today's groups

| from | to | seam | direction | model | asked for by |
|---|---|---|---|---|---|
| `9170632` | `adfa272` | planner | toward code | Opus 5 | the agent, from a token ceiling; kept by the user |

## The line

Which exercises the planner may pick from. Before: the whole space allowed by equipment, time and exclusions (119 with dumbbells). After: only exercises whose primary muscles fall in the groups today's workout trains (14 for a leg day).

## How it was declared

In the commit message: "the split is declared by the user in `training.toml`, so *today trains legs and core* is a fact about today in the way today's equipment is. What the engine still does not decide is which of the admissible exercises to prescribe, in what order, or for how long."

## Note

This is the constraint [E1](../E1-adaptation-bound-to-the-slot/README.md) later carried into adaptations, where the user's words, not the split, say what today trains.
