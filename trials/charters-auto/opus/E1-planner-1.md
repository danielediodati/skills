# planner charter

Input: a `plans.Request` (equipment, minutes, exclusions, groups, allocation, preferences, refusals) or a `plans.MesocycleRequest` (one `Request` per slot, plus refusals), assembled by `plans.requested` before any model call.
Output: a validated `WorkoutPlan` or `Mesocycle`, offered through an `interrupt`; accepted, it is written as a prescribed workout (or kept mesocycle); refused by the validator to the end, the run closes `refused` with nothing offered.

## Free
- Which admissible exercises go in the plan: choosing is the deliberation ADR-0001 keeps out of the engine.
- Workout structure (block count, straight sets vs superset vs circuit, order): ADR-0001 rules out structure menus; no rule says what a good workout is yet (issue 11.02, needs-info, waiting on the user's methodology).
- Rounds and reps or seconds per exercise, and the unit for each: the schema only makes the unit one of two, so the wrong state cannot be written.
- Rest per block: prescribed by the model and recorded; the bands in `PLANNING` are a reference, never checked (ADR-0001 rules out a fixed rest).
- The reason on every block, and the `why` on every `despite` row: the part of a plan only the agent can supply; code checks only that it is non-empty.
- How the time divides over the groups: `allocation` is an even split offered as a starting point, `allocate` divides on any proportions, and nothing checks the plan followed it.
- Covering every requested group with a primary-muscle exercise: asked in the brief, measured by the eval's `_does_not_degenerate`, never refused by the validator.
- Proposing an exercise the user would rather not do: allowed, if the plan says so in `despite` (TRAINER.md invariant 4: the user answers by refusing).
- How a new proposal differs from the ones turned down: only the identical one is refused; how different is the agent's business (ADR-0007 item 5).
- How many cycles a mesocycle runs, and why: the agent's choice with a reason, like rest (ADR-0008 item 2); code checks `cycles >= 1` and a non-blank `why`.
- Which tools to call, in what order, how many up to the budget: the model plans over the tools; the prompt asks it not to explore for its own sake.

## Constrained
- Every `exercise_id` is in today's `admissible_set`: held twice, as an `enum` in the strict emit schema and by the validator re-reading the set, so the two cannot disagree. Exclusions are safety and are filtered out before the model sees the set.
- Mesocycle emit schema holds ids to the union of every slot's admissible set; which slot admits which id is left to the validator, because the workouts share one item schema.
- Today's constraints are folded into a single-workout request once, in `turn`, before the brief: the emit schema and the validator both read the request, and applied on one side only they would describe different spaces. Not done for a mesocycle request.
- The plan fits the declared minutes: over budget is refused whole, never trimmed (ADR-0001), so the agent learns the arithmetic was wrong. Under budget is accepted.
- The plan lands within `TOLERANCE_MIN = 5` minutes either side of the request: a 25-minute plan for a 45-minute ask is not the workout asked for (issue 11.03, user's decision). Not yet in code, which refuses only over and accepts any plan under.
- The requested minutes never exceed `duration_cap_min` in `training.toml`: refused, not clamped, so the engine never decides how long someone trains.
- An exercise appears at most once in a workout (may repeat across mesocycle workouts): the engine cannot cost a plan naming one twice.
- A preferred-against exercise without a `despite` row is refused, and a `despite` row for an exercise the user never refused is refused: silence is the failure, and an invented refusal would be printed back as the user's words.
- A plan identical to one already turned down is refused: the newest refusal compared as the whole document, earlier ones on their exercise ids in order (what the negotiation keeps of them, ADR-0007 item 4).
- A mesocycle has exactly one workout per slot, in split order, each validated as that slot's single workout; a mismatch in count is refused before anything else.
- Validator order: duplicates and admissibility first, budget only if both pass, then preferences and refusals: so a bad id is named as an id, not as an uncostable plan.
- Shape: strict JSON schema, `extra="forbid"` everywhere, at least one block and one item, non-empty reasons, `rest` in seconds and `rounds` as full passes: a misspelled field silently ignored would be a different workout that validates; a unit nobody named once cost a run (`rest: 60000`).
- What the plan is made against (equipment, time, exclusions) is never in the plan: a plan that declared its own budget could declare one it fits.
- Validator refusals go back to the model verbatim, every broken rule named, through `FEEDBACK`: the model fixes the plan knowing why (ADR-0004).
- A provider-refused turn goes back to the model as `REFUSED_TURN`, telling it to write strict JSON with literal numbers: two observed failures (`22/45`, truncated call) that otherwise lost a whole run.
- A quota error is raised at once, never retried: every retry is refused the same way.
- The tool surface is a named list, `TOOLS`, without `prescribed_workout`: a planner has no workout to read back, and a derived list would let a renamed tool arrive unchosen.
- Catalog records reach the model cut to `KEEPS = (id, equipment, primary_muscles)`: a model shown `name` copied it into `exercise_id`.
- A bad tool call comes back as a failed tool result, not an exception: the model can correct it next turn.
- Turning a plan down ends the run and starts a fresh one with cleared messages and the brief rewritten carrying every refusal: a new proposal, not an argument with the last (ADR-0007). A shorter time in the answer replaces the budget and drops the allocation.
- Accepting writes the prescribed workout; an accepted mesocycle is kept and nothing is prescribed until served (ADR-0005, ADR-0008 item 4).
- Mesocycle brief states exclusions and preferences from the first slot only; the validator checks each slot against its own.

## Budget
- Tool calls: `tools.CALL_BUDGET = 12` per run, overridable by `--call-budget`; past it the model is called without tools and must emit. A budget, not a principle.
- Emits: `ATTEMPTS = 3` per run; a plan still refused after the third ends the run with nothing offered. Today's value, tested through the constant.
- Provider refusals: `REJECTIONS = 2` in a row, reset by the first accepted turn; the third raises. Counted in a row so isolated hiccups across validator retries do not end a recovering run.
- Model calls per run: one per planner turn (at most budget + rejections + attempts turns) plus one structured emit per attempt.
- Reasoning: `models.REASONING = "low"` for planning models, chosen for wall time on the dev laptop (`high` 296 s vs 39 s); never measured in plan quality (issue 11.02).
- Eval: `trainer eval --suite plan`, six situations, six legality invariants, bar 100%. It measures legality, not whether a plan is good.
