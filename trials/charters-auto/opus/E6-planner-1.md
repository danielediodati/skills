# planner charter

Input: a `plans.Request` (one workout, possibly an adaptation of today's mesocycle slot) or a `plans.MesocycleRequest` (one request per slot, possibly changing or continuing a mesocycle), plus the user's live conclusions from the store.
Output: a validated `WorkoutPlan`, `AdaptedPlan` or `Mesocycle` offered through an `interrupt`; once accepted, a prescribed workout or a kept mesocycle written to the database. A run the validator refuses to the end offers nothing.

## Free
- Which exercises, inside the admissible set: ADR-0001, the engine says what is possible and the agent what is good.
- How many blocks, their order, and straight sets / superset / circuit: workout structure is method, which no rule may decide (ADR-0001).
- Rounds, reps or seconds per exercise, and the unit: method; code only refuses what the engine cannot cost (rounds under one, negative rest).
- Rest per block: ADR-0001 rules out a fixed rest; the methodology's bands are a reference.
- Where the plan lands inside the methodology's ranges for the goal column: the prompt hands over ranges, "not a template".
- How the minutes divide over the groups: `allocation` is an even split offered as a starting point, `allocate` is there to redo it, and nothing checks the plan kept it.
- Each block's `reason`, in its own words: "the part of the plan only you can supply"; code only requires it non-empty.
- Covering every group once before a second block for any of them: asked in the brief, not checked; only "each group has one primary exercise" is.
- Proposing an exercise the user would rather not do, with a `despite` row saying why: a preference is knowledge, not safety, and TRAINER.md's invariant is "says so and asks", not "never".
- How a new proposal differs from the ones turned down: `_not_a_plan_already_refused` refuses only the identical answer; how different is the agent's business.
- How to weigh the user's conclusions: given with their quotes, explicitly "none of it is a rule".
- Which tools to call, in what order and how many, up to the budget: the prompt only asks not to explore for its own sake.
- For an adaptation: the time, the groups, the equipment and which workout to start from, read off what the user said: nothing of the mesocycle binds it, and the validator skips the budget and untrained rules.
- For an adaptation: `counts_as` among the workouts still to do, and the `note` text: closest workout is a judgement.
- For a mesocycle: how many cycles and the one-sentence `why`: the prompt says "that number is yours to choose"; ADR-0001.
- For a change: what to keep and what to rewrite beyond what the user asked: the prompt says "keeping the rest" and code compares nothing.
- Using at least two movement patterns when more are on offer: measured by `trainer eval` (`not degenerate`), never refused by the validator (ADR-0001, degeneration is measured, not forbidden).

## Constrained
- Every exercise id is in `admissible_set` for today's request: held twice, as an `enum` in the strict emit schema and by the validator, because the space is the engine's (ADR-0001) and an invented id is never prescribed. For an adaptation the enum is dropped (the whole catalog is an enum Anthropic refuses) and the validator alone holds it.
- Today's exclusions, budget and groups are folded into the request once in `turn` via `constraining_today`: the emit schema and the validator must read the same space.
- Exclusions are filtered out before the model sees the set: safety, not a preference, so not negotiable.
- The plan lands within `TOLERANCE_MIN` = 5 minutes either side of the budget, short refused as surely as long: the rule itself, also the `time` invariant. Never trimmed or padded (ADR-0001: a silent repair hides the error from the agent). Skipped for an adaptation.
- Every requested group gets an exercise whose primary muscles are in it, when the admissible set can train it (`untrained`): moved into the validator after it was the one invariant Haiku missed (ADR-0011). Skipped for an adaptation.
- An exercise appears at most once in a workout: the engine cannot cost a plan that names one twice.
- A preference prescribed without a `despite` row is refused, and a `despite` row for something the user never refused is refused: silence is the failure, and an invented refusal would be printed back as the user's words.
- A plan identical to one turned down is refused; earlier refusals, narrowed to their ids, refuse the same ids in the same order (ADR-0007, the memory a negotiation keeps).
- An adapted plan's `counts_as` is one of the workouts still to do this cycle.
- A mesocycle has exactly one workout per slot, each validated as that slot's single workout; on a change `cycles` is at least the current cycle; `cycles` >= 1 and `why` non-blank.
- The plan's shape is a closed pydantic schema (`extra="forbid"`, strict JSON schema, every field required): a misspelled field quietly ignored would be a different workout that validates.
- Units are fixed: `rest` in seconds, `prescription` as one `unit` (reps or seconds) and one `amount`: the wrong state cannot be expressed; an observed `rest: 60000` cost a run.
- The plan does not carry its own budget, equipment or exclusions: the request does, so a plan cannot declare one it fits.
- The tool surface is a named list of ten, without `prescribed_workout`: named, not derived, so a rename cannot silently add a tool.
- Exercise records returned by tools keep only `id`, `equipment`, `primary_muscles`, `mechanic` (`KEEPS`).
- A refused plan goes back with every violation named, in the validator's order, and the model tries again: the check is code and is not argued with.
- After `ATTEMPTS` refusals the run ends `refused` and offers nothing: no fallback plan, no partial one.
- A turn the provider refuses goes back to the model as `REFUSED_TURN`, at no attempt's cost; a quota error is raised at once; past `REJECTIONS` consecutive refusals the error is raised.
- An emission that is not JSON is the provider's failure: asked again at no attempt's cost, and past `REJECTIONS` in a row it raises `ProviderFailed`.
- Nothing is written until the user accepts (ADR-0005): the run stops at `interrupt`. An accepted mesocycle is kept and nothing is prescribed until served (ADR-0008); an accepted adaptation is recorded as today's serving.
- A turned-down plan ends its run and starts a new one in the same negotiation, messages cleared and the brief rewritten carrying every refusal; a shorter time asked for drops the allocation (ADR-0007).
- The model is chosen in code, not by the seam: `PLANNER_CHOICE` = `anthropic/claude-haiku-4.5`, no effort, host `anthropic`, the cheapest that clears the plan suite's 100% bar (ADR-0011). Overridable by `PLANNER_MODEL` / `PLANNER_HOST`.
- The plan suite's bar is 100% on its invariants: an invariant broken is a bug, not a tuning knob (ADR-0010).

## Budget
- Tool calls: `tools.CALL_BUDGET` = 12 per run, a default that `--call-budget` raises; when spent, tools are unbound and the model is asked to emit with what it knows.
- Plans: `ATTEMPTS` = 3 emissions per run before a refusal ends it; the prompt tells the model the number.
- Provider refusals: `REJECTIONS` = 2 in a row, reset by the first accepted turn; a value tuned to observed failures, not a design limit.
- Model calls: one per planner turn, plus one `emit` per attempt (strict structured output, tools not bound).
- Cost: ~$0.05-0.13 and ~35-47 s a two-slot mesocycle on the chosen model, with a prompt-cache breakpoint (ADR-0011).
