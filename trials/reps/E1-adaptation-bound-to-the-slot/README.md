# E1 - The adaptation bound to the slot

| from | to | seam | direction | model | lived in | strength |
|---|---|---|---|---|---|---|
| `674648c` | `1057b2a` | planner, adaptation | toward code (substitution, then templating) | Opus 5.5 | code, 10 days | strong |

## The line

Who decides what an adapted workout trains, with what, and for how long. An adaptation is today's workout re-planned from what the user says about it (*«oggi niente gambe»*, *«solo 30 minuti»*).

- **Design**: ADR-0008 item 6 and ticket 10.3. The planner reads the user's words; the mesocycle's workout is **the starting point**.
- **Drifted state**: code decides. The adaptation request is today's slot request, so its groups, its admissible set (filtered to those groups and to the declared equipment) and its budget bind. Another workout of the cycle is refused outright. From `491f084` the validator also refuses a plan that leaves out one of the slot's groups ([D5](../D5-an-untrained-group-refused/README.md)). In session 14 the entrance becomes a form-filler: five fields (`minutes`, `equipment`, `leave_out`, `ask_for`, `workout`) that code checks before and after planning.
- **How it showed**: *«oggi niente gambe»* on a legs day is a dead end. The request holds only leg exercises and the validator refuses any plan without legs.

## The commits

| commit | date | what |
|---|---|---|
| `a706cba` Close ticket 10.3 | 2026-09-22 | `plan.adaptation_requested` builds today's slot request and raises `PlanRejected("an adaptation is of the workout the rotation is at; naming another one plans it from nothing")`. Its docstring still says "starting point". |
| `f087624` Open session 14 | 2026-10-01 | The spec: "the user's sentence, plus the fields code can check". |
| `af0302b` Ticket 14.3 | 2026-10-01 | The five fields, refused before planning and checked by the validator after. |
| `1057b2a` Ticket 14.4 | 2026-10-02 | **The correction**, asked by the user ([D3](../D3-the-adaptation-handed-back-to-the-planner/README.md)). |

## Declared?

Not as a move. Ticket 10.3 says "starting point"; the code made it binding without saying so. The session 14 spec writes the fields down, against what the user had said in the grilling that produced it.

## The user's corrections

Paraphrased.

- 2026-10-01, during the grilling: the proposal is a state machine again; the model must tell from context whether a change is for today or for good; no fixed slots.
- 2026-10-02, on the first paid pass: with *«oggi niente gambe»*, what reaches the planner is ETL again. Rules on rules end in dead ends; the planner must put the user's will first.

The agent's own reading, same session: the 14.3 design makes the entrance a form-filler, and its proposal led straight there.

## Entry points for a replay

- **1** (cleanest): [request.md](request.md), at `674648c`.
- **2**: ticket 14.3 at `4122bf0`. Weaker: the ticket names the fields, so the drift is in the request.

## What a replay looks for

Whether the adaptation's request binds the slot's groups, equipment or budget, or refuses another workout of the cycle, where ticket 10.3 asked only for a starting point.
