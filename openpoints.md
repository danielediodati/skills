# Open points

What is still undecided or undone. Decisions already taken are in `CONTEXT.md` and `docs/adr/`; work that has a ticket is in `ROADMAP.md`; standing limits are in `CONTEXT.md`, Known limits. Delete a point when it closes.

## Waiting for a decision

- **A charter written from the code makes the agent stop on changes the user wants.** 10 and 13 stops in 24 trials with the two charters an agent wrote, because nobody told it which of today's behaviours are defects (`trials/results-auto-charter.md`, `trials/results-practice-charter.md`). Only the user's charter did. What the plugin does about it is undecided: nothing, or a review by the user of what the code does not show.
- **Whether the rule in `AGENTS.md` names the three moves agents do not see as moves:** input cleaned by code before the model reads it, a parsing rule that also catches a free field, a missing field defaulted instead of refused. `edd` names them in its diff check; the rule, always in context, does not. Changing the rule changes what sessions 5 and 6 measure.

## Work no ticket covers

- **The `eval` skill**: to write. Cases, graders, judge calibration, the core and extended sets, the dev and held-out splits, the target and the eval direction now in `eval.md`. Finished only when the cases cover every line of the charter and each grader has been seen to fail an output.
- **`setup`** does not yet copy the eval scripts or create `evals/`.
- **The root `README.md`** has to teach the vocabulary through one example, start to finish. Sessions 5 and 6 give it its numbers; the example has no ticket.
- **Not measured:** a draft reviewed by the user against a charter written with the user.
