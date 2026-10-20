# planner charter

Input: a `plans.Request` (one workout: equipment, minutes, groups, offered allocation, exclusions, preferences, goal, refusals so far, an adaptation) or a `plans.MesocycleRequest` (one request per slot, refusals, a change or a continuation), plus the user's live conclusions from the store.
Output: a `WorkoutPlan` or `Mesocycle` that passed the validator, proposed through an `interrupt`; accepted, code writes it as a prescribed workout, an adapted serving or a kept mesocycle. Or no plan: the run ends `refused` after its last attempt.

## Free
- Which exercises, inside the admissible set: method is the agent's (ADR-0001); the engine only says what is possible.
- How many blocks, their order, and straight sets, superset or circuit: workout structure is deliberation, not a rule (ADR-0001).
- Rounds, the amount, and reps or seconds per exercise: the methodology gives ranges, "where the plan lands inside them is your decision".
- Rest per block: ADR-0001 rules out a fixed rest value; the bands are a reference.
- The reason on each block: "the part of the plan only you can supply"; code only requires it non-empty.
- How the minutes divide over the groups: the even allocation is offered, `allocate` takes any proportions, and nothing checks the plan kept it (`Request.allocation`).
- Which tools to call, in what order and how many, within the call budget: the model knows what it needs to find out.
- Whether to propose an exercise the user would rather not do, with a `despite` row saying why: a preference is not an exclusion, and the user answers by refusing.
- How a new proposal differs from the ones turned down: "how is the agent's business"; a rule on how different would be the validator deciding method.
- How to weigh the user's conclusions: given to the model with their quote as "none of it is a rule"; the admissible set is the same without them.
- What an adaptation keeps of the slot it starts from, beyond what was asked for and left out: "keep what still fits".
- How many cycles a mesocycle runs, and why: "That number is yours to choose" (ADR-0008).

## Constrained
- Every exercise is in today's `admissible_set`: held twice, by an `enum` in the emit schema and by the validator, because legality is held at 100% (ADR-0010). Exclusions are filtered out before the model sees the set.
- Today's constraints (`constraining_today`: exclusions, minutes, groups) are folded into the request once, before the brief: the schema and the validator must describe the same space.
- The plan lands within `TOLERANCE_MIN` = 5 minutes of the minutes asked for, either side, and is refused, never trimmed or padded (ADR-0001): a silent repair hides the arithmetic from the agent. The 5 is the rule's value; the prompt, the brief and `remaining_budget` all read the constant.
- An exercise appears at most once in a workout (across a mesocycle's workouts it may repeat): `plan_seconds` cannot cost a duplicate.
- Each group asked for gets an exercise whose primary muscles are in it, unless the admissible set has none (`untrained`): moved into the validator after it was the eval's only failure on Haiku (ADR-0011).
- A preference prescribed without a `despite` row is refused, and a `despite` row for something the user never refused is refused: TRAINER.md's fourth invariant, *says so and asks*, made checkable.
- A plan equal to one already turned down is refused: the newest refusal compared whole, older ones by their exercise ids in order, because that is all the negotiation keeps of them (ADR-0007).
- An adaptation holds every exercise asked for and none left out; an exercise asked for outside the request's admissible set is refused before the model runs (`_admits`).
- A mesocycle has exactly one workout per slot, `cycles` >= 1, a non-blank `why`, and on a change `cycles` >= the cycle it is in: each workout is validated as that slot's single workout.
- A mesocycle's schema enum is the union of every slot's admissible ids; which slot admits which is the validator's to say, because the workouts share one item schema.
- A mesocycle's goal, exclusions and preferences in the brief are read from the first slot.
- Shape: strict JSON schema, `extra="forbid"`, `unit` is `reps` or `seconds` with one `amount`, `rest` in seconds, `reason` non-empty, at least one block and one item: the wrong state cannot be expressed, which beats telling the model not to write it.
- Validation is code, never a model judge; duplicates and admissibility first, time and groups skipped when either fails, so the message names the real mistake.
- Every violation goes back to the model verbatim (`FEEDBACK`), and the model plans again.
- The tool surface is a named list of ten; `prescribed_workout` is left out, and named rather than derived so no tool arrives without a decision. Exercises come back with `KEEPS` only: id, equipment, primary muscles, mechanic.
- The plan is emitted by a separate structured-output call (`emit`) after the tool loop, with tools unbound.
- A provider refusing a turn goes back to the model as `REFUSED_TURN`; text from `emit` that is not JSON is asked for again without spending an attempt (the host's decoder failed, not the model); a quota error is raised at once.
- The prompt, the brief's wording, the methodology (without its sources) and the goal's column are fixed by code; the allocation is labelled a starting point, not an instruction.
- A turned-down plan ends its run; the next run in the same negotiation starts with cleared messages and the refusals carried, and a shorter time the user gave drops the allocation.
- Only an accepted plan is written, and code writes it; nothing is written before the `interrupt`, because a resumed node runs again from the top.
- The model is `anthropic/claude-haiku-4.5`, effort none, on Anthropic via OpenRouter: the cheapest configuration that clears the plan suite at 100% (ADR-0011); `PLANNER_MODEL`, `PLANNER_REASONING`, `PLANNER_HOST` override it.

## Budget
- Tool calls: `CALL_BUDGET` = 12 per run, counted per call and not reset between attempts; `--call-budget` overrides it. Past it the tools are unbound and the model must emit. A budget, not a rule.
- Attempts: `ATTEMPTS` = 3 emissions validated per run; after the third refusal the run ends with no plan. The prompt states the number.
- Provider refusals: `REJECTIONS` = 2 in a row, reset by the first accepted turn; the third is raised.
- Runs per negotiation: not capped in code; each refusal by the user starts another.
- Cost and time: ~$0.13 and ~47 s a two-slot mesocycle (ADR-0011); $0.052 with prompt caching on `--only no-equipment`.
- Output tokens: `GROQ_MAX_TOKENS`, default 1000, on Groq only, reasoning included.
