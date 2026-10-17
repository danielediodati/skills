# planner charter

Input: a `plan.Request` (one workout: equipment, minutes, groups, allocation, exclusions, preferences, refusals, optional adaptation) or a `plan.MesocycleRequest` (one `Request` per slot, refusals, optional change or continuation), assembled by `plan.requested` and its siblings before the model is called.
Output: a validated `WorkoutPlan` or `Mesocycle` offered at an interrupt; accepted, a prescribed workout, an adapted serving or a kept mesocycle in SQLite; otherwise a run closed as refused or turned down.

## Free
- Which exercises, among today's admissible ids: choosing is the point of the agent (ADR-0001); code only draws the space.
- How many blocks, their order, and straight sets, superset or circuit: workout structure is method, which the engine never prescribes (ADR-0001).
- Rounds and the amount per exercise: method; code only holds both to at least 1.
- Reps or seconds for each exercise: the model knows a plank from a push-up; the shape lets it state exactly one.
- Rest per block: the bands in `PLANNING` are a reference, not a rule (ADR-0001 rules out a fixed rest); code only refuses a negative one.
- The reason on every block, and the one-sentence `why` of a mesocycle: "the part of the plan only you can supply"; a fixed reason would make the field decoration.
- How the minutes divide over the groups: the brief's even split is offered, and `allocate` takes any proportions; nothing checks the plan kept it (`Request.allocation`).
- Whether every requested group gets an exercise with that group as primary, and coverage before a second block: told in the brief, measured by `trainer eval` (`does not degenerate`), never refused by the validator; ADR-0001 rules out coverage rules.
- Whether to propose an exercise the user would rather not do: a preference is knowledge of the person, not safety; allowed with a `despite` row, so the user can say no again.
- How a new plan differs from the ones turned down: code refuses only an identical one; a rule on how different would be code deciding method.
- What an adaptation keeps of today's slot and what it changes, and what a change keeps of the mesocycle: the brief asks to keep what still fits; nothing checks it.
- How many cycles a mesocycle lasts: "That number is yours to choose" (ADR-0008), above the floors in Constrained.
- Which tools to call, with which arguments, and how many, up to the call budget: the model plans over the engine; `PLANNING` asks it not to explore for its own sake.
- When to stop calling tools and emit: a turn with no tool call goes straight to emit.

## Constrained
- Every `exercise_id` is in today's `admissible_set`: the emit schema's enum holds it to those ids and `validate` refuses any other; legality is never the model's (ADR-0010 keeps it at 100%).
- A mesocycle's enum is the union of every slot's admissible ids; which slot admits which id is the validator's call: the workouts share one item schema.
- The plan fits the minutes, costed by the engine (`duration.plan_duration`): over is refused whole, never trimmed (ADR-0001); a silent cut would hide the arithmetic from the agent.
- An exercise appears at most once in a workout (`duration.check_plan`); the same exercise may appear in two workouts of a mesocycle.
- The validator checks in a fixed order: duplicates, then admissibility, then time only if both passed, then preferences, then refusals. Every broken rule goes back in one message, so the model is told what to fix rather than "it cannot be costed".
- A preferred-against exercise without a `despite` row is refused, and a `despite` row for an exercise the user never refused is refused: TRAINER.md's fourth invariant, and the renderer would otherwise print an invented refusal as the user's words.
- A plan identical to one the negotiation turned down is refused: the newest compared whole, earlier ones on their exercise ids in order; a mesocycle compared whole or on its ids per slot. That is what the negotiation keeps of them (ADR-0007).
- A mesocycle has exactly one workout per slot, in the split's order, or nothing else is checked.
- `cycles` is at least 1, and on a change at least the cycle in progress: a change keeps the count.
- Wire shape is strict (`extra="forbid"`, every property required): a misspelled field quietly ignored is a different workout that validates. At least one block, at least one item, a non-empty `reason`; `Mesocycle.why` is also refused when blank. Not yet blank-checked for a block's `reason`, which accepts whitespace.
- `Prescription` is a unit (`reps` | `seconds`) and an amount: both-or-neither cannot be expressed.
- Units are stated in the schema: `rest` in seconds after each round, never ms or minutes; `rounds` from the top. An observed `rest: 60000` lost a run.
- A document that is not JSON or not the shape is refused as `shape` and costs an attempt like any rule.
- `ATTEMPTS = 3` emitted plans per run; the third refusal ends the run as refused and nothing is offered. The number is in the prompt, so moving it changes what the model is told.
- `REJECTIONS = 2` consecutive provider refusals of a turn, reset by the first accepted; the third is raised. Each one goes back as `REFUSED_TURN` asking for strict JSON. A model that cannot produce an acceptable turn twice running will not on the third.
- An exhausted quota (`models.spent`) is raised at once, never retried: every retry is refused the same way.
- Tool calls are capped by `tools.CALL_BUDGET` (12, `--call-budget` overrides); past it the model is called without tools and then asked to emit. A budget, not a constraint on method: the value can be raised.
- The emission is a separate structured call (`json_schema`, strict) after the tool loop, with the fixed line `EMIT_PLAN` or `EMIT_MESOCYCLE`: by construction it is a document, not prose.
- The tools offered are the named list `TOOLS`, without `prescribed_workout`: a planner has no prescription to read back. Named, not derived, so a renamed tool is never gained silently.
- Every exercise record a tool returns is cut to `KEEPS` (`id`, `equipment`, `primary_muscles`): a model shown `name` copied it into `exercise_id`, and every field is re-read on every turn.
- A tool call the model got wrong (unknown tool, bad arguments, an engine failure) comes back as a failed result, not a crash: the model can correct it next turn.
- Today's standing exclusions and the duration cap are folded into a single-workout request once, at the first turn, so the emit schema and the validator read the same space. Exclusions are safety and are removed from the space, never left to the model.
- Minutes over `training.toml`'s cap are refused, never clamped: clamping is the engine deciding how long somebody trains.
- The system prompt and the brief are written once per run, only when the run has no history: a non-empty history means the brief is already there.
- What the model is told comes from fixed templates (`PLANNING`, `MESOCYCLE_PLANNING`, `brief`, `mesocycle_brief`, `adapted`, `changed`, `continued`, `turned_down`, `FEEDBACK`): the rules stated there are the ones the validator applies (`test_the_prompt_carries_the_rules_the_validator_will_apply`).
- The group-coverage rule is written into the brief only when the request names groups: stated always, it read as "cover them all" and blew the time on a 15-minute request.
- A mesocycle brief takes exclusions and preferences from slot 1 only.
- Nothing is written before the user answers: the plan stops at an `interrupt` (ADR-0005). Accepted, it becomes exactly one prescribed workout, or an adapted serving when adapting, or a kept mesocycle that prescribes nothing (ADR-0008).
- Turning a plan down ends that run and starts a fresh one in the same negotiation: messages cleared, the brief rewritten with every refusal (newest whole, earlier as ids) and what the user said. A fresh proposal, not an argument with the last.
- "Shorter" from the user replaces the minutes and drops the allocation, which divided the old minutes.
- `said` outlives every run on the thread; everything else a run holds is reset when the next begins (ADR-0006, ADR-0007).
- Every run is closed into the archive given to `build`, and a graph built without one keeps nothing: eval runs must not become the user's history.
- The model is `PLANNER_MODEL` on the provider `LLM_BACKEND` names, falling back to the coach's, with effort from `PLANNER_REASONING`: chosen by environment, never by the run.

## Budget
- Calls: up to 3 attempts, each a tool loop of model turns plus one emit call; tool calls capped at 12 per run (raisable); up to 2 consecutive provider refusals per turn.
- Output: `GROQ_MAX_TOKENS`, default 1000 per turn, reasoning included; today's value of Groq's free tier, the first number to raise on a paid one.
- Context: every tool answer is re-read on every later turn, so `KEEPS` and asking `admissible_set` for today's groups are what keep it small.
- Seconds and cost: no cap in code; measured per node in the run record and in the eval matrix (ROADMAP session 12).
