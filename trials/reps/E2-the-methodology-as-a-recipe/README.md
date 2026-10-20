# E2 - The methodology written as a recipe

| from | to | seam | direction | model | lived in | strength |
|---|---|---|---|---|---|---|
| `a9b2c50` | `ddb48bb` | planner's prompt | toward code (templating) | Opus 5.5 | uncommitted draft, 1 day | strong |

## The line

How many exercises and sets a muscle group gets, and how a session is shaped. Ticket 11.2 has the planner read a methodology document in both its prompts, so whatever that document fixes, the planner no longer chooses.

- **Design**: TRAINER.md, "constrain the form, never the content"; the agent "chooses the tools, the exercises, their order and the rest". The planner's choice, inside ranges.
- **Drifted state**: a draft `docs/methodology.md`, never committed, with per-session counts (chest, back and legs 2-3 exercises and 8-12 sets; arms, shoulders and core 1-2 and 4-8) and a fixed order to fill spare time. In the grilling that followed, the agent derived a general rule from the user's own plan: the main muscle about 4 exercises and 12-13 sets, the secondary 2 and about 6, four roles in every session.

## The commits

| commit | date | what |
|---|---|---|
| none | 2026-09-24 | The draft, on disk only. |
| `ddb48bb` Write the methodology the planner will reason with | 2026-09-25 | **The correction**: ranges per goal, and principles. Its message: "a first draft that fixed exercise counts per muscle and a session shape was overfitting one person's plan". |

## Declared?

No. The draft was the agent's first answer.

## The user's corrections

2026-09-24/25, paraphrased:

- The counts are wrong: legs are not one muscle, and the method must serve every goal.
- How much a group gets is the planner's decision, made per request. At most ranges, depending on how the user wants to train and the time given. The rest of the agent's questions are overfitting.

## Caveat for a replay

The ticket lists "how many exercises a group gets" among what the methodology must say, in the same sentence that calls it "the user's own methodology, which is not the agent's to invent". Part of the drift is in the request.

## What a replay looks for

Whether the document fixes counts of exercises or sets per group or per session, or a fixed session shape, rather than ranges the planner chooses inside.
