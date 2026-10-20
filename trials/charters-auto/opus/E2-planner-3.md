# planner charter

Input: a `plan.Request` (one workout: equipment, minutes, groups, allocation, exclusions, preferences, refusals, optional `adapting`) or a `plan.MesocycleRequest` (one request per slot, refusals, optional `changing` / `continuing`), assembled by `plan.requested` and its siblings before the model is called.
Output: a validated `WorkoutPlan` or `Mesocycle` offered to the user through an `interrupt`; on acceptance a prescribed workout, an adapted serving or a kept mesocycle written by code; on three refusals by the validator, a run closed as `refused` with nothing offered.

## Free
- Which exercises, among the admissible ones: ADR-0001, the engine says what is possible and the agent what is good.
- The workout's structure (blocks, straight sets vs superset vs circuit, order): ADR-0001, no split menus or structure rules in the engine.
- Rounds, and reps vs seconds per exercise with their amount: method, left to the agent; only the unit list is closed (see Constrained).
- Rest per block: ADR-0001 rules out a fixed rest; the bands in `PLANNING` (3 min / 90-120 s / 60 s) are a reference, never checked.
- How the minutes divide over the groups: the even `allocation` is offered "as a starting point and not an instruction", and nothing checks it was followed.
- Covering every asked group with a primary-muscle exercise, and covering each once before a second block: asked in the brief only; ADR-0001 rules out coverage rules, so it is measured by the eval's `does not degenerate` invariant, not refused.
- Each block's `reason`, and each `despite.why`: the part of the plan only the model can supply (TRAINER.md); code only requires it non-empty.
- Proposing an exercise the user would rather not do: allowed with a `despite` row; a preference is knowledge of the person, not safety.
- How a new proposal differs from the turned-down ones: code refuses only an identical plan (or, for older refusals, the same ids in the same order); "how different" would be code deciding method.
- Which tools to call, how many (within the budget), in what order, and when to stop exploring and emit: a turn with no tool calls goes straight to emit.
- How many cycles a mesocycle runs, and its one-sentence `why`: "That number is yours to choose" (ADR-0008); bounded only below.
- What to keep from today's mesocycle slot when adapting, and what to rewrite for the cycles left when changing: the prompt frames it, code checks only the usual rules.

## Constrained
- The tool surface is the named tuple `TOOLS` (ten tools, no `prescribed_workout`): named, not derived, so no tool arrives without someone deciding it should.
- Tool answers are trimmed to `KEEPS` (`id`, `equipment`, `primary_muscles`): `name` beside `id` was copied into `exercise_id`.
- Every `exercise_id` is in today's admissible set: held twice, by an `enum` in the emit schema at decoding time and by `_every_id_admissible` after; legality is 100% (ADR-0010). For a mesocycle the enum is the union of the slots and the validator holds each slot to its own set.
- Exclusions (standing and given), equipment and groups are folded into the request by code before the model sees it; the brief tells the model they are already filtered out, and it cannot add or drop one.
- The minutes: refused above the declared cap, never clamped (`within_the_cap`); the plan must cost within them per the engine's `plan_duration`, and is refused whole, never trimmed (ADR-0001).
- An exercise appears at most once per workout (`duplicates`); the same exercise may recur across mesocycle slots.
- The wire shape is strict: `extra="forbid"`, at least one block and one item, `unit` is `reps` or `seconds` only, `rest` in seconds, `reason` non-empty, `despite` a list on the plan, not per item. Each was a failure seen in a run (milliseconds rest, invented refusals on every item).
- `despite` may name only exercises in `request.preferences`; a preferred-against exercise prescribed without a row is refused: TRAINER.md's fourth invariant, "says so and asks".
- A plan identical to a turned-down one is refused (`refused`); for a mesocycle, also the slot count must equal the split's, and when changing, `cycles` is at least the current cycle.
- Validator order is duplicates, admissibility, then budget (skipped if either failed), then preferences and refusals; every broken rule goes back to the model in one message (`FEEDBACK`).
- A document that is not JSON or not the shape is a `shape` violation and spends an attempt like any other.
- Attempts: `ATTEMPTS = 3` emitted plans per run; then the run closes as refused and nothing reaches the user. A budget that may be raised, not a rule.
- Provider refusals: up to `REJECTIONS = 2` in a row are fed back as `REFUSED_TURN` and retried, the count resetting on the first accepted turn; the third raises. A quota error raises at once, since every retry is refused the same way.
- Tools are unbound once `spent >= budget`, and a tools turn that reaches the budget goes straight to emit: the model is asked for the plan with what it knows.
- Emitting is a separate structured-output call (`json_schema`, strict) after the tool loop; the model never writes the plan as prose.
- Acceptance is the user's (`propose` interrupts); the model never writes. Only `prescribe` records, on today's date from `date.today()`.
- A turned-down plan ends the run; the next run starts with messages cleared, the brief rewritten with every refusal (the newest whole, earlier ones as ids), and a shorter `minutes` replacing the budget and dropping the allocation.
- Which model and effort: `PLANNER_MODEL` / `PLANNER_REASONING` from the environment, else the coach's model; never chosen by the seam.
- For a mesocycle, the brief states exclusions and preferences from the first slot only.

## Budget
- Budget: `CALL_BUDGET = 12` tool calls per run (overridable with `--call-budget`, today's value of a budget). Calls are counted per tool result, so one turn may overshoot it. Model calls per run: one per planner turn plus one emit per attempt, up to 3 attempts, plus up to 2 retried provider refusals in a row. No limit in code on seconds, tokens or cost; the eval suite reports tokens, and any run that reaches a paid model needs the user's approval first (CLAUDE.md).
