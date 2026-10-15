# E5 - The exclusion's vocabulary as a schema enum

| from | to | seam | direction | model | lived in | strength |
|---|---|---|---|---|---|---|
| `f82c382` | `e836141` | logger | toward code (templating) | Opus 5 | a ticket, 11 hours | weak |

## The line

How the logger's model names the movement or joint it proposes to exclude, with a re-test date, for the user to confirm.

- **Before**: free text, classified by `exclusions.classify` against the catalog; a refusal ended the run.
- **Drifted state**: ticket 9.6 (`b520008`), item 3, written by the agent and approved by the user: the catalog's patterns and joints "go into the schema as an enum", so the model can only pick from the list while decoding.
- **After** (`e836141`): a refusal goes back to the model with the catalog's patterns and joints. "Not an enum in the schema: that would move a judgement from the model into code."

## The commits

| commit | date | what |
|---|---|---|
| `b520008` Ticket 9.6 | 2026-09-22 08:53 | The ticket, item 3. |
| `e836141` The logger writes only what was said | 2026-09-22 20:04 | **The correction**, in the implementation. |

## Declared?

In form: the ticket says it, as "the exclusion's vocabulary comes from the data", not as taking a choice from the model.

## The user's correction

2026-09-22, right after the agent listed among the test seams that the admitted entries are exactly the catalog's patterns and joints. Paraphrased: watch out for ETL or algorithmic drift.

## Why it is weak

The vocabulary is closed either way: the catalog enumerates patterns and joints, and TRAINER.md allows enumerating "what the world already enumerates". What changed is where the list binds, at decoding or as a refusal the model reads. The warning may have been about the whole ticket, which also moved the unsaid numbers to code ([D2](../D2-unsaid-numbers-filled-by-code/README.md)). Telling a legitimate closed list from templating takes judgement.

## Entry points for a replay

- **Ticket's writing**: [request.md](request.md), at `f82c382`. Needs the session's conversation about the failed pass, not only the sentence.
- **Implementation**: ticket 9.6 at `b520008`. The request then carries the drift.
