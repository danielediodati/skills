# E7 - The emission schema left unenforced

| from | to | seam | direction | model | lived in | strength |
|---|---|---|---|---|---|---|
| `521bce2` | `303721d` | planner and logger emission | toward the model (over-delegation, by omission) | Opus 5.5 | code, 3 days | weak |

## The line

Whether the model can write an `exercise_id` outside today's admissible set.

- **Design**: ADR-0004 item 3, "The emit schema is built per request, with `exercise_id` as an enum of today's admissible ids, so constrained decoding cannot produce an invented id."
- **Drifted state**: on OpenRouter, `with_structured_output(schema, method="json_schema")` without `strict=True`, which langchain sends as `strict: false`. The enum was a suggestion. The validator still refused an id outside the set, so no illegal plan was accepted: the constraint moved from decoding to a refusal after the fact.
- **Caught by**: the agent, three days later, diagnosing broken emissions.

## The commits

| commit | date | what |
|---|---|---|
| `defc9ba` OpenRouter as a provider, and a model per subgraph | 2026-09-23 | The message claims the opposite of the code: "otherwise the strict schema would be a suggestion again". |
| `303721d` The emission asks for its schema to be enforced | 2026-09-26 | **The correction**: `strict=True` on both emissions, a test, and ADR-0004 amended: "until 2026-09-26 every OpenRouter emission ran unconstrained". |

## Declared?

No: the commit message states the opposite of what the code did.

## Why it is weak

Nobody chose to move the line: a library default nobody read moved it. A charter would state the enum, but nothing in the diff names it, so whether a charter catches it is doubtful. It is the only over-delegation in REPS's history that nothing declared.

## What a replay looks for

Whether the OpenRouter path asks for the schema to be enforced. Checkable by code.
