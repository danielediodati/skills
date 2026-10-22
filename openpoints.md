# Open points

What is still undecided or undone. Decisions already taken are in `CONTEXT.md` and `docs/adr/`; work that has a ticket is in `ROADMAP.md`; standing limits are in `CONTEXT.md`, Known limits. Delete a point when it closes.

## Waiting for a decision

- **Whether the rule in `AGENTS.md` names the three moves agents do not see as moves:** input cleaned by code before the model reads it, a parsing rule that also catches a free field, a missing field defaulted instead of refused. `edd` names them in its diff check; the rule, always in context, does not. Changing the rule changes what sessions 5 and 6 measure.
  - Session 5 adds a fourth, the one behind both drifts with a draft: **code works out the answer and the prompt hands it over.** On `action_items 06` code computed a calendar of the days after the meeting and the prompt told the model to read the date off it, on a line every draft held as the user does. The rubric names it; `edd`'s diff check does not. Whether `edd` and the rule name it is part of the same decision. Haiku's one drift with a draft, in session 6, is the same move on the same request.

## Work no ticket covers

- **The `eval` skill**: to write. Cases, graders, judge calibration, the core and extended sets, the dev and held-out splits, the target and the eval direction now in `eval.md`. Finished only when the cases cover every line of the charter and each grader has been seen to fail an output.
- **`setup`** does not yet copy the eval scripts or create `evals/`.
- **A seam added during development** gets no charter by itself: `setup` lists the seams once, and the rule in `AGENTS.md` sends the agent to a charter before it changes a seam, not when it creates one.
