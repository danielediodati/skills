# planner charter

Input: a `plan.Request` (equipment, minutes, groups, allocation, exclusions, preferences, refusals) or a `plan.MesocycleRequest` (one `Request` per slot, plus refusals), built by `plan.requested` / `plan.mesocycle_requested`; on resume, an `Answer` (accepted, or turned down with `because` and optional `minutes`).
Output: a validated `WorkoutPlan` or `Mesocycle` offered through `interrupt`; on acceptance, a prescribed workout or a kept mesocycle written to the DB; otherwise a run closed as `refused` or `turned_down`.

## Free
- Which exercises, among the admissible set: ADR-0001, the engine says what is possible and the agent what is good.
- Block structure (straight sets, superset, circuit), rounds and order of blocks: method, which ADR-0001 keeps out of code.
- Reps or seconds per exercise, and the amount: method; code only fixes that it is exactly one of the two.
- Rest per block: the prompt's bands (about 3 min heavy, 90-120 s hypertrophy, 60 s isolation) are a reference, not a rule (ADR-0001 rules out a fixed rest).
- How the time divides over the groups: the even `allocation` is offered as a starting point; `allocate` may divide it otherwise and nothing checks that it did not.
- Covering every requested group with a primary-muscle exercise, once before any second block: asked in the brief only, no validator rule; ADR-0001 rules out coverage rules, degeneration is measured by the volume deficit instead.
- Whether to propose an exercise the user would rather not do: allowed, if a `despite` row says why (TRAINER.md's fourth invariant: say so and ask).
- How a new plan differs from the ones turned down: the agent's business; code refuses only the identical plan.
- The `reason` of each block and the `why` of a `despite` row: the part only the model can supply.
- Which tools to call, in what order, and when to stop and emit: the planning loop is the model's, within the call budget.
- A mesocycle's number of cycles and its `why`: the prompt says the number is the model's; the shape only requires `cycles >= 1` and a non-blank `why`.

## Constrained
- Tool surface: exactly the ten names in `TOOLS`, listed by name and never derived by subtraction, so no tool arrives undecided; `prescribed_workout` is left out because a planner has no workout to read back.
- Tool answers are cut to `KEEPS` (`id`, `equipment`, `primary_muscles`): `name` is hidden because a model shown both copied it into `exercise_id`.
- A bad tool call (unknown tool, wrong arguments, `ToolFailure`) goes back to the model as a failed result, not raised: the model can correct it next turn.
- Standing exclusions, the duration cap and the groups are folded into the request once, before the first turn, so emit schema and validator check the same space. Mesocycle runs skip this fold and use the slots as `mesocycle_requested` built them.
- Emission is a separate call with strict `json_schema` structured output, every `exercise_id` an enum of today's admissible ids (for a mesocycle, the union over slots; which slot admits which id is the validator's).
- Plan shape: `extra="forbid"` everywhere, at least one block and one item, `prescription` as `unit` in {reps, seconds} plus `amount`, `rest` and `rounds` as integers with their units in the schema (a `rest: 60000` run was lost to an unstated unit), `despite` a list on the plan, not a field per item (a per-item field made a model invent refusals).
- A plan with no `budget`/request fields: what the plan was made against is the request, so a plan cannot declare a budget it fits.
- Validator rules, all code, in this order: `shape`, `duplicates` (an exercise at most once per workout), `admissible` (membership read from `admissible_set` itself), `budget` (costed duration <= minutes; skipped when the first two failed), `preferences` (a preference prescribed without a `despite` row, or a `despite` row for something the user never refused), `refused` (identical to a turned-down plan; older refusals compared on exercise ids in order).
- Mesocycle validator: exactly one workout per slot, in order (`slots`), each checked as that slot's single workout, then refused if identical to a turned-down mesocycle. The same exercise in two slots is allowed.
- Nothing is trimmed or repaired: a plan over budget is refused whole and sent back with the reason (ADR-0001), so the arithmetic error stays visible to the agent.
- Validator feedback goes back to the model as a `validator` message naming every violation; the run ends `refused` after `ATTEMPTS` = 3 emitted plans with no offer to the user.
- A provider refusing a turn (invalid JSON in a tool call, truncation) goes back to the model as `REFUSED_TURN`; after `REJECTIONS` = 2 in a row the error is raised. The count resets on the first accepted turn, so isolated hiccups across retries do not end a recovering run. A quota error (`models.spent`) is raised at once: every retry would be refused the same way.
- When the call budget is spent the model is invoked without tools and then asked to emit: the run always reaches a plan rather than exploring further.
- A validated plan is always offered to the user (`interrupt`, ADR-0005); nothing is written before an answer.
- Accepted: a single plan becomes a prescribed workout dated today, block reasons kept; a mesocycle is kept and nothing is prescribed (ADR-0008, item 4).
- Turned down: the run closes `turned_down` and a new run follows in the same negotiation with messages cleared and the brief rewritten (ADR-0007). The newest refusal travels whole, earlier ones only as exercise ids. A shorter `minutes` replaces the budget and drops the allocation; for a mesocycle `minutes` is ignored.
- The brief's wording is code: it states the equipment, minutes, groups, allocation, exclusions (already filtered out), preferences and refusals, and tells the model not to argue or offer something token after a refusal. A mesocycle brief takes exclusions and preferences from the first slot only.
- Archive: a run is archived only when `build` is given an `archive`; eval suites build without one so their runs do not become the user's history.
- One model for every node; planning models are asked for `reasoning="low"` (in `models`, not here).

## Budget
- Tool calls: `tools.CALL_BUDGET` = 12 per run, a default that `--call-budget` and `build(budget=...)` override; stored in the state so a cut run can be read back.
- Emitted plans: `ATTEMPTS` = 3 per run, stated to the model in the prompt; the code gives no reason for 3, so read it as today's value of a budget.
- Provider refusals: `REJECTIONS` = 2 in a row per run.
- Model calls per run: one per planning turn (at most budget + attempts + rejections turns) plus one emit per attempt.
- Output tokens: Groq `max_tokens` defaults to 1000 (`GROQ_MAX_TOKENS`), the free-tier ceiling, shared with reasoning; on a paid tier it is the first number to raise. Ollama context length comes from `OLLAMA_CONTEXT_LENGTH`.
- Turned-down runs per negotiation: no cap in code.
