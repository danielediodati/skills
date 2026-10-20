# planner charter

Input: a `plan.Request` (one workout) or `plan.MesocycleRequest` (one `Request` per slot), assembled by code from the declarations, the rotation, today's constraints and the negotiation's refusals; plus the user's live conclusions from the store.
Output: a `WorkoutPlan` or `Mesocycle` that passed the validator, offered to the user through an `interrupt`; accepted, code records it as a prescribed workout (or a kept mesocycle). A run the validator refuses to the end offers nothing.

## Free
- Which exercises, inside the admissible set: what makes a workout good is the agent's, the engine only says what is possible (ADR-0001).
- The workout's structure: block count and order, straight sets, superset or circuit (ADR-0001, ADR-0002).
- Rounds, reps or seconds per exercise, and the amount: the methodology gives ranges, not a template.
- Rest per block: no fixed rest value, the bands are a reference (ADR-0001).
- Each block's `reason`: the one part of the plan only the model can supply (TRAINER.md).
- Where the plan lands inside the goal's methodology column: the prompt hands over the ranges and says the position is the model's.
- How the minutes divide over the groups: the even `allocation` is offered as a starting point, `allocate` divides on any proportions, and nothing checks it was followed.
- Order of group coverage and how many blocks a group gets: the brief asks *cover each once before a second block*; code checks only that each is trained.
- Weekly volume across a mesocycle's workouts: the prompt says the sets per muscle add up; no rule reads it.
- Whether to propose an exercise the user would rather not do, with a `despite` row saying why: a preference is knowledge of the person, not safety (TRAINER.md invariant 4).
- How a new proposal differs from the ones turned down: what makes the second plan better is the agent's business; code refuses only a repeat.
- How much weight the user's conclusions get: they are context, not rules, and the admissible set is the same without them.
- In an adaptation, everything beyond `asked_for` and `left_out` (a superset, *one more per group*, *you choose*): kept as prose for the planner (spec 14).
- In a mesocycle change, what to keep and what to rewrite for the cycles left.
- How many cycles a mesocycle repeats for, and the sentence why (ADR-0008): the prompt says the number is the model's.
- Which tools to call, in what order, and when to stop calling and emit: the budget bounds it, the model spends it.

## Constrained
- The tool set is a closed, named list of ten (`TOOLS`), and `prescribed_workout` is left out: derived by subtraction, a renamed tool would arrive unasked and the registry guard would not see it.
- Tool answers are trimmed to `id`, `equipment`, `primary_muscles`, `mechanic` (`KEEPS`): what a plan is written from, and less context per call.
- Tools read only; nothing the model calls writes: the engine records a workout, a tool never does.
- The request is built by code (`plan.requested`), never by the model: equipment, minutes and groups fall back to declarations and rotation, so a plan is checked against the request that was made.
- Today's constraints (exclusions, budget, groups) are folded into the request once, at the run's first turn: the emit schema and the validator both read it, and applied on one side only they would describe different spaces.
- Exclusions are filtered out of the admissible set before the model sees it; they are safety, never the model's to weigh.
- The emission is strict `json_schema` structured output of `WorkoutPlan` / `Mesocycle`, with every `exercise_id` an enum of today's admissible ids (a mesocycle: the union over its slots, the per-slot check is the validator's): an id outside the space cannot be written.
- The shape forbids extra fields, needs at least one block and one item, a non-empty `reason`, and a prescription that is `reps` or `seconds` with one `amount`: the wrong state cannot be expressed, and a misspelled field is not silently dropped.
- `rest` is seconds and `rounds` counts from the top, stated in the schema: an observed `rest: 60000` lost a run over a unit nobody had told the model.
- The plan carries no budget, equipment or exclusions of its own: a plan that declared its own budget could declare one it fits.
- `despite` is one list on the plan, not a field on every item: per item, a model filled all eight with refusals the user never made.
- Every exercise is in the admissible set, decided by membership in `admissible_set` itself: a second reading of the same `WHERE` would one day disagree.
- The plan runs within `TOLERANCE_MIN` = 5 minutes either side of the minutes asked, short as surely as over: the rule is the window; 5 is today's width, written once in `plan.py` and quoted to the model.
- A plan that does not fit is refused, never trimmed or padded: a silent repair hides the arithmetic error from the agent (ADR-0001).
- No exercise twice in one workout; the same exercise may appear in two workouts of a mesocycle.
- Every group asked for has an exercise whose primary muscles are in it, unless today's admissible set has none: moved into the validator after Haiku passed it and the eval did not (ADR-0011).
- A `despite` row names only an exercise the user actually said no to, and a preferred-against exercise without one is refused: silence is the failure, not the choice.
- A plan equal to one already turned down is refused: the newest refusal compared whole, earlier ones by their exercise ids in order, because only the ids are kept of them.
- In an adaptation, every `asked_for` id is held and no `left_out` id is: the fields code can check (spec 14); asking never widens the admissible set, and an excluded id is refused before the run.
- A mesocycle has exactly one workout per slot, in the split's order; `cycles` is at least 1, and at least the current cycle when changing one; `why` is not blank.
- The validator runs in a fixed order (duplicates and admissibility first, then budget and groups, then the request's rules) and returns every violation at once: the clock is skipped when it cannot cost the plan, and the model sees each rule it broke.
- Violations go back to the model verbatim, under a fixed `FEEDBACK` frame; a document that is not a plan comes back as one `shape` violation.
- `ATTEMPTS` = 3 emissions per run; the third refused ends the run as `refused` with nothing offered: handing back the same plan changes nothing, and `trainer eval` never reaches an interrupt.
- Provider refusals of a turn are retried with a fixed `REFUSED_TURN` message, up to `REJECTIONS` = 2 in a row, reset by the first accepted turn, then raised: a model that fails twice running will not on the third, and isolated hiccups do not end a recovering run.
- An emission that is not JSON costs no attempt and is asked for again, up to the same `REJECTIONS`, then `ProviderFailed`: under a strict schema that is the host failing, not the model deciding.
- A quota error is raised at once, never retried: every retry is refused the same way.
- Acceptance is the user's, through an `interrupt` (ADR-0005); the model never decides a plan is accepted.
- Turning a plan down ends that run and starts a new one in the same negotiation, messages cleared and the brief rewritten with every refusal; a shorter time asked for drops the allocation (ADR-0007).
- An accepted workout is written by code as a prescribed workout (an adaptation as today's serving); an accepted mesocycle is kept and nothing is prescribed until served (ADR-0008).
- The plan suite holds six invariants at 100% over every run: an invariant broken is a bug, not a tuning knob (ADR-0010).
- The model is ADR-0011's choice, `anthropic/claude-haiku-4.5`, no effort, host `anthropic`, the cheapest that clears the plan suite's bar; moving it is a new matrix row, then the rule reapplied.

## Budget
- Tool calls: `CALL_BUDGET` = 12 per run, `--call-budget` overrides it: a budget, not a rule. Checked between turns, so one turn's parallel calls may pass it; once spent, tools are unbound and the run goes straight to emit.
- Model calls: one planner turn per tool round, one `emit` per attempt, at most 3 attempts, plus up to 2 provider retries in a row on either.
- Cost and time: ~$0.13 and ~47 s a two-slot mesocycle on the choice (ADR-0011); ~$0.05 with the prompt-cache breakpoint, of which `emit` is ~$0.015 because it binds no tools and cannot read the cached turns.
