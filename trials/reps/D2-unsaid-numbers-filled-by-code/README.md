# D2 - The numbers nobody said are filled by code

| from | to | seam | direction | model | asked for by |
|---|---|---|---|---|---|
| `b520008` | `e836141` | logger | toward code | Opus 5 | the agent's ticket 9.6, approved by the user |

## The line

A number inside a block the user named but did not give (*«military, 2 serie»*, reps unsaid). Before: the model writes it, copied from the prescription and labelled `assumed`, because the strict schema requires every field. After: the model leaves it `null` and `log.to_performed` writes the prescribed value as `assumed`.

## How it was declared

ADR-0009, *The agent writes what was said*: the model writes what the user said or answered, the engine what is assumed. Ticket 9.6 item 1 and the commit message both name the move. The same ticket carried [E5](../E5-the-exclusion-vocabulary-as-an-enum/README.md).
