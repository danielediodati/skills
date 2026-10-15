# D5 - A group asked for and never trained is refused

| from | to | seam | direction | model | asked for by |
|---|---|---|---|---|---|
| `37c57a7` | `491f084` | planner | toward code | Opus 5.5 | the agent, from a screening |

## The line

Whether a workout may leave out a group its slot asks for. Before: the eval's sixth invariant checked it and the validator did not, so the model was never told. After: the validator refuses it (`untrained`) and sends it back, and the eval calls the validator instead of keeping a copy. The pattern axis stays eval-only, with the reason given.

## How it was declared

In the commit message, with the measurement behind it: Haiku's one screening failure and two of DeepSeek's.

## Note

This is the rule that made [E1](../E1-adaptation-bound-to-the-slot/README.md)'s dead end visible: *«oggi niente gambe»* on a legs slot was refused for training no legs.
