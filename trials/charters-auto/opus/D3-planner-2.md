# planner charter

Input: a `plans.Request` (one workout) or `plans.MesocycleRequest` (one `Request` per slot), assembled by `plans.requested` and its siblings; the user's live conclusions from the store; on later runs, the refusals of the same negotiation.
Output: a validated `WorkoutPlan` or `Mesocycle`, offered through an `interrupt`; accepted, a prescribed workout or a kept mesocycle in the database; or a run closed `refused` with no plan.

## Free
- Which exercises, out of the admissible set: ADR-0001, the engine says what is possible and the agent what is good.
- The workout's structure (straight sets, supersets, circuits), block order, rounds, reps or seconds and their amounts: method is the agent's (ADR-0001); the methodology gives ranges, not a template.
- Rest per block: ADR-0001 rules out a fixed rest value; the bands are a reference.
- How the minutes divide over the groups: `Request.allocation` is an even split offered as a starting point, and nothing checks the plan followed it.
- Where inside the goal's methodology column the plan lands: the prompt hands it over as "your decision".
- The one-sentence `reason` per block: the part of the plan only the model can supply (TRAINER.md); code only requires it non-empty.
- Proposing an exercise the user would rather not do, with a `despite` row saying why: a preference is knowledge, not safety, and the user answers it by refusing.
- How the next plan differs from one turned down: code refuses only an identical plan (or the same ids, for older refusals); a rule on *how* different would be code deciding method.
- How much weight the user's conclusions get: the brief says none of it is a rule and the admissible set is the same without it.
- Which tools to call, in what order, and when to stop calling and emit: the call budget caps the count, not the choice.
- How many cycles a mesocycle repeats, and why: the prompt says the number is the model's; the shape asks only `cycles >= 1` and a non-blank `why`.
- Covering every group once before giving one a second block: asked in the brief, not checked by code.

## Constrained
- Every `exercise_id` is in today's `admissible_set`, held twice: an `enum` in the strict emit schema and the validator's membership check. Legality is held at 100% (ADR-0010).
- A mesocycle's emit schema has one enum, the union of every slot's set; which slot admits which id is the validator's: the workouts share one item schema.
- Exclusions, equipment, today's time and groups are folded into the request by code (`constraints.constraining_today`) before the brief is written, and the same request feeds the schema and the validator: applied on one side only they would describe different spaces.
- The plan lands within `TOLERANCE_MIN` = 5 minutes either side of the budget, refused both under and over and never trimmed or padded: ADR-0001 rules out an automatic cut, because a silent repair hides the arithmetic from the agent. The 5 is the rule's width, not a budget.
- An exercise appears at most once in a workout (may repeat across a mesocycle's workouts): the engine cannot cost one twice.
- Every group asked for gets an exercise whose **primary** muscles are in it, when the admissible set has one (`untrained`): moved into the validator after Haiku left a group untrained (ADR-0011).
- The wire shape is fixed: `extra="forbid"`, `unit` in `reps | seconds` with one `amount`, `rest` in seconds, `items` and `blocks` non-empty, `despite` a plan-level list: each closed an observed failure (a misspelled field ignored, `rest: 60000`, invented refusals on every item).
- A `despite` row naming an exercise the user never refused is refused, and a preference prescribed without one is refused: TRAINER.md's fourth invariant, *says so and asks*.
- A plan identical to one the negotiation turned down is refused; older refusals are compared on their exercise ids only, which is all the negotiation keeps of them (ADR-0007).
- An adaptation holds every `asked_for` id and none of `left_out`; asked-for ids outside the admissible set are refused before the model runs: asking never widens the set.
- A mesocycle has exactly one workout per slot, in the split's order; a change keeps `cycles` at least the current cycle, since `cycles` is the total.
- A mesocycle's goal, exclusions and preferences in the brief are read off the first slot only.
- The tools are a named list of ten, without `prescribed_workout`: named, not derived, so no tool arrives without someone deciding it.
- Tool answers are projected to `KEEPS` (`id`, `equipment`, `primary_muscles`, `mechanic`): what a plan is written from.
- A model mistake in a tool call (unknown tool, bad arguments) returns as a failed result the model can recover from; anything else propagates.
- Planning and emitting are separate calls: `emit` binds no tools and uses strict `json_schema` structured output.
- Validator refusals go back to the model naming every rule broken, up to `ATTEMPTS` = 3 plans a run; the third refused ends the run `refused` with nothing offered.
- A provider refusing a turn, or emitting non-JSON under the strict schema, costs no attempt and is retried with what the provider said, up to `REJECTIONS` = 2 in a row, then raised; the count resets on the first accepted turn. A spent quota is raised at once.
- Turned down by the user, the run closes and a fresh run starts on the same negotiation with messages cleared and the brief rewritten carrying the refusal; a shorter time asked for replaces the budget and drops the allocation.
- Nothing is written to the database before acceptance; an accepted plan is recorded as prescribed (or adapted, or a kept mesocycle) by code, never by the model.
- The model is `PLANNER_CHOICE` (`anthropic/claude-haiku-4.5`, effort none, host `anthropic`) unless the environment names another: the cheapest configuration that clears the plan suite's 100% (ADR-0011).

## Budget
- Tool calls: `tools.CALL_BUDGET` = 12 per run, overridable with `--call-budget`; today's value, not a rule. When spent, tools are unbound and the model is asked to emit with what it knows.
- Plans: 3 attempts per run (`ATTEMPTS`). Provider refusals: 2 in a row (`REJECTIONS`).
- Runs per negotiation: unbounded; each refusal by the user starts one more.
- Cost and time (ADR-0011): ~$0.13 and ~47 s a two-slot mesocycle; ~$0.052 with a prompt-cache breakpoint, of which `emit` is ~$0.015. No wall-clock limit in the graph.
- Output per turn, on Groq only: `DEFAULT_MAX_TOKENS` = 1000, shared with reasoning, Groq's free-tier ceiling; `GROQ_MAX_TOKENS` raises it.
