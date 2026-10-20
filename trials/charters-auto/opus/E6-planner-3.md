# planner charter

Input: a `plans.Request` (one workout, or an adaptation of today's mesocycle workout) or a `plans.MesocycleRequest` (one request per slot, possibly changing or continuing a mesocycle), assembled by code in `plan.py`, plus the user's live conclusions from the store.
Output: a validated `WorkoutPlan` / `AdaptedPlan` / `Mesocycle` offered to the user at an interrupt; once accepted, a prescribed workout or a kept mesocycle written to the database. If not, a run closed as `REFUSED` or `TURNED_DOWN`, or a provider error raised.

## Free
- Which exercises, taken from the admissible set: this is method, and ADR-0001 keeps method away from the engine.
- Block structure (straight sets, superset, circuit), rounds, and the order of the blocks: same reason. The prompt asks that each group is covered once before any gets a second block; no code checks it.
- Reps or seconds for each exercise, and how many: the shape only lets one unit be picked. Choosing it is judgement.
- Rest per block: ADR-0001 rules out a fixed rest value, and the bands are only a reference.
- The one-sentence `reason` per block: the shape requires it because only the model can supply it (TRAINER.md).
- Where the plan lands inside the methodology's ranges for the goal column: the prompt hands over ranges, not a template.
- How the minutes divide over the groups: `allocation` is an even split, offered as a starting point. `allocate` re-divides on any proportions and nothing checks which split was used.
- Which tools to call, in what order, and when to stop and emit (within the call budget): the model knows what it is missing, and the prompt tells it not to explore for its own sake.
- How much weight the user's conclusions get: they are told to the model as "none of it is a rule", and the admissible set is the same without them.
- Whether to propose an exercise the user would rather not do, and why: a preference is knowledge of the person, not safety (TRAINER.md invariant 4). Only doing it silently is refused.
- How a new proposal differs from the ones turned down: ADR-0007 item 5 keeps the weakest reading, so how different it is stays the agent's business.
- Mesocycle: how many cycles and the sentence why (ADR-0008 item 2), like a block's rest. The same exercise may appear in two slots.
- Mesocycle change: what to rewrite from the user's words and what to keep.
- Adaptation: how to read what the user said. Time, groups, equipment and which exercises go in or out are all the planner's, because no validator rule reads the words (ADR-0008 item 6). The model also picks which still-to-do workout it `counts_as`, and writes the `note`.

## Constrained
- The request (equipment, minutes, groups, rotation slot, exclusions, preferences, goal) is assembled by code before the model is called, and the validator checks against that same object. Assembled in two places, the two would drift and the plan would be checked against a request nobody made. The model never picks the groups or the slot, except in an adaptation.
- Today's constraints (`constraining_today`) are folded into the request once, at the first turn. If they were applied to only one of the emit schema and the validator, the two would describe different spaces.
- Exclusions are filtered out of the admissible set by the engine and cannot be argued with: they are safety, not preference.
- Every `exercise_id` is in today's admissible set. For a single workout this is enforced twice, by an enum in the strict emit schema and again by the validator. For a mesocycle the schema enum holds the union of all slots and the validator checks each slot. For an adaptation the validator alone holds it, because Anthropic will not compile an enum of the whole catalog.
- The plan runs within `TOLERANCE_MIN` = 5 minutes either side of the budget, and nothing is trimmed or padded to fit (ADR-0001: a silent repair hides the arithmetic from the agent). The no-repair rule is fixed. The 5 is today's tolerance. Not applied to an adaptation, whose time is the planner's.
- No exercise appears twice in one workout: `plan_seconds` cannot cost a duplicate.
- Every requested group gets at least one exercise whose primary muscles are in it, unless the admissible set has none for it (`untrained`). This rule moved into the validator after Haiku left a group untrained (ADR-0011). Not applied to an adaptation.
- An exercise the user would rather not do needs a `despite` row, and a `despite` row may name only one of those exercises. Without the first, a re-proposal would be silent. Without the second, the model invents refusals that the renderer would print back as the user's own words.
- A plan identical to one the negotiation already turned down is refused. The newest refusal is compared as a whole document, the earlier ones by their ordered exercise ids. That is the weakest reading available (ADR-0007).
- An adapted plan's `counts_as` must be one of the cycle's workouts still to do, or the rotation breaks.
- Mesocycle: exactly one workout per slot, each validated as that slot's single workout. On a change, `cycles` is at least the cycle in progress. `cycles` ≥ 1 and `why` is not blank. Beyond that, the count is the agent's (ADR-0008).
- In a mesocycle brief, exclusions, preferences and goal are read from the first slot only.
- Output shape: strict JSON schema with `extra="forbid"`. `unit` is `reps` or `seconds`, `rest` is seconds, `reason` is non-empty, there is at least one block and at least one item. Each choice comes from a lost run: a misspelled field silently ignored, both-or-neither units, `rest: 60000` taken as milliseconds, a `despite` field on every item filled with invented refusals.
- Pipeline order: tool turns, then a separate structured `emit` call, then a deterministic `validate`, then `propose` (interrupt), then `prescribe`. The model reasons with tools, but only the strict emission is taken as the plan.
- The tool surface is the ten names in `TOOLS`, listed by name. `prescribed_workout` is left out: the planner has no prescription to read back, and a rename would otherwise hand it the tool without anyone deciding to. Tools never write.
- Tool results are trimmed to `KEEPS` (`id`, `equipment`, `primary_muscles`, `mechanic`), which is what a plan is written from.
- A bad tool call (unknown tool, arguments that do not fit, `ToolFailure`) goes back to the model as a failed result rather than a traceback, so the model can fix it on its next turn.
- A validator refusal goes back to the model with every violation it found (`FEEDBACK`), until `ATTEMPTS` runs out. After that the run ends as `REFUSED` with nothing offered.
- A provider refusing a turn goes back to the model as `REFUSED_TURN`, telling it to write strict JSON with literal numbers. An emission that is not JSON is asked for again without spending an attempt, since under a strict schema that is the host failing, not the model. Both count against `REJECTIONS` in a row, and the count resets on the first accepted turn. A quota error is raised at once, because every retry would fail the same way.
- Accepting a plan is the user's decision, never the model's. Nothing is written until they accept (ADR-0005). An accepted mesocycle is kept and not prescribed: a workout is prescribed only when it is served (ADR-0008 item 4).
- Turning a plan down ends the run. The next run starts with cleared messages and a rewritten brief that carries every refusal. A shorter time asked for replaces the budget and drops the allocation.
- The methodology the model reads is the committed document without its sources (`for_planner`). The goal column is the declared goal.
- Model: `anthropic/claude-haiku-4.5`, effort none, host `anthropic`, by ADR-0011's rule: the cheapest configuration that clears the plan suite's 100% bar (ADR-0010). `PLANNER_MODEL` / `PLANNER_REASONING` / `PLANNER_HOST` override it.

## Budget
- Tool calls: `CALL_BUDGET` = 12 per run, overridable with `--call-budget`. This is a budget, not a rule. When it runs out, tools are unbound and the model is asked for the plan with what it knows.
- Validator attempts: `ATTEMPTS` = 3 per run. A budget.
- Provider refusals and non-JSON emissions: `REJECTIONS` = 2 in a row, then the error is raised. A budget.
- Model calls per run: one per tool turn (at most `CALL_BUDGET` + 1 before the forced emit), plus one `emit` per attempt, plus re-asks under `REJECTIONS`.
- Cost and time (ADR-0011): about $0.13 and about 47 s for a two-slot mesocycle. A single workout costs about $0.052 with the prompt-cache breakpoint, 12 calls, 34 to 38 s. `emit` is the largest single call.
- Output tokens: `GROQ_MAX_TOKENS` (default 1000) caps a turn only on Groq.
