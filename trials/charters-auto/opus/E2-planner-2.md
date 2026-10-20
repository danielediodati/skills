# planner charter

Input: a `plans.Request` (one workout: equipment, minutes, groups, offered allocation, exclusions, preferences, refusals, optional mesocycle slot to adapt) or a `plans.MesocycleRequest` (one `Request` per slot, optional mesocycle being changed or continued), assembled in code by `plans.requested` and its siblings.
Output: a validated `WorkoutPlan` or `Mesocycle` proposed through an `interrupt`; accepted, it is written as a prescribed workout, an adapted serving, or a kept mesocycle. A run refused three times ends with nothing proposed.

## Free
- Which exercises, among the admissible ones: choosing the method is the agent's, the engine only bounds the space (ADR-0001).
- The workout's structure: number of blocks, straight sets vs superset vs circuit, order. ADR-0001 rules out split menus and structure rules; ticket 11.2 waits on the user's methodology before anything here is fixed.
- Rounds, the amount, and whether an exercise counts reps or seconds: method, not legality.
- Rest per block: the prompt's bands are a reference, not a rule (ADR-0001 rules out a fixed rest).
- Each block's `reason`: the one part only the model can supply (TRAINER.md); code only requires it non-empty.
- How the minutes divide over the groups: the even `allocation` is offered as a starting point, `allocate` takes any proportions, and nothing checks it (ADR-0001, no time ratios).
- Covering every requested group with a primary-muscle exercise, each once before any gets a second block: asked in the brief, never validated (ADR-0001 rules out coverage rules); only the eval's `_does_not_degenerate` measures it.
- How much of the time to use, as long as it does not run over: today a 25-minute plan of 45 is valid. Constrained by the user below, not yet in code.
- Which tools to call, in what order, with what arguments, within the call budget: deliberation is the model's; failed calls come back as results it can correct.
- Proposing an exercise the user would rather not do, with a `despite` row saying why: a preference is knowledge of the person, not safety (TRAINER.md fourth invariant).
- How a re-proposal differs from the plans turned down: a rule on *how* different would be code deciding method; only an identical one is refused.
- In an adaptation, what of today's slot to keep and what to change; in a change, what of the mesocycle to rewrite: asked in the brief, not checked.
- A mesocycle's `cycles` and its `why`: the prompt says the number is the model's to choose (ADR-0008).
- Reading what the user said (`said`, `because`): free text, passed through as written.

## Constrained
- Every `exercise_id` is in today's `admissible_set`: enforced twice, as an `enum` in the emit schema and by the validator reading the set itself (not a second `WHERE`). Hard; held at 100% (ADR-0010).
- Today's exclusions, budget and groups are folded into the request once, by `constraints.constraining_today`, before the brief: the emit schema and the validator must describe the same space.
- The plan runs no longer than `budget_min`, costed by the engine; over is refused whole, never trimmed (ADR-0001). Hard.
- The plan lands within 5 minutes either side of the declared time (`plan.TOLERANCE_MIN = 5`), refused with a distinct message for under and for over, and the prompt says the number: user's decision, ticket 11.3, so a 25-of-45 plan stops passing. Not yet in code, which refuses only over and accepts any plan under.
- An exercise appears at most once per workout (`duration.check_plan`); in a mesocycle, at most once per workout but free across workouts. Hard.
- The document's shape: strict JSON schema, every field required, `extra="forbid"`, at least one block and one item per block, `unit` in `reps|seconds`, `rest` an integer in seconds, `reason` non-empty. Each shape choice answers an observed failure (`rest: 60000`, both-or-neither reps/seconds, misspelled fields read as written). A shape error is a `shape` violation, never a traceback.
- `despite` lists exactly the preferred-against exercises the plan names: one prescribed silently is refused, one listed that the user never refused is refused (an observed run invented eight).
- A plan identical to one turned down in this negotiation is refused: compared whole against the newest, by exercise-id sequence against earlier ones, which are kept only as ids (ADR-0007).
- Mesocycle: exactly one workout per slot, in the split's order; each checked as that slot's own plan; `cycles >= 1`, `why` not blank; on a change, `cycles` at least the current cycle.
- The mesocycle emit schema's `enum` is the union of every slot's admissible ids; which slot admits which is left to the validator.
- Validation order: duplicates, then admissibility, the clock only if both pass, then preferences and refusals. Every violation goes back to the model verbatim, in one message.
- Attempts: 3 emitted plans per run, then the run ends `refused` with nothing proposed. A run-level cap, read with ADR-0010's 100% bar; today's value, not argued as a law.
- The tool surface is a named list of ten; `prescribed_workout` is left out because a planner has no workout to read back. Named, not derived by subtraction, so a renamed tool cannot slip in unchosen.
- Exercise records reach the model trimmed to `id`, `equipment`, `primary_muscles`: a model shown `name` copied it into `exercise_id`.
- Planning and emitting are two calls: the tool loop ends when the model stops calling tools or the budget is spent, then a separate structured-output call (`json_schema`) emits the document. The model cannot skip the emit or emit without the schema.
- A provider refusal of a turn is turned into a message asking for strict JSON, up to 2 in a row (reset on the first accepted); the third is raised. A spent daily quota or credits is raised at once: every retry would be refused the same way.
- The request is assembled in code, never by the model: equipment named or declared, minutes named or the declared cap (above the cap is refused, not clamped), groups off the rotation, allocation an even split, preferences checked against the catalog. Mesocycle briefs state exclusions and preferences from the first slot only.
- A valid plan is proposed and nothing is written until the user accepts (ADR-0005). Turning it down closes the run and starts a fresh one in the same negotiation: messages cleared, brief rewritten with every refusal; a shorter time replaces the budget and drops the allocation.
- On acceptance: a workout is recorded as prescribed, an adaptation as today's serving with the mesocycle untouched, a mesocycle is kept and nothing prescribed until served (ADR-0008).
- Which model and effort: `PLANNER_MODEL` / `PLANNER_REASONING`, falling back to the coach's provider and model; on Ollama `reasoning="low"` (296 s at high against 39 s on the dev laptop, never measured in plan quality). Chosen by ticket 12.4's matrix, not by the seam.
- Prompts are English; the date is `date.today()`.

## Budget
- Tool calls: 12 per run (`tools.CALL_BUDGET`), overridable with `--call-budget`. A budget value: when spent, tools are unbound and the model is told to emit with what it knows.
- Model calls per run: one per planning turn (at most 12 tool calls, plus up to 2 refused turns in a row) and one emit per attempt, at most 3 attempts; each turn the user refuses starts a new run with the same budget.
- Tokens: `DEFAULT_MAX_TOKENS = 1000` per turn on Groq, reasoning included, set by the free-tier ceiling; on a paid tier it is the first number to raise (`GROQ_MAX_TOKENS`).
- Seconds: no time limit in code.
- Cost: no per-run cap in code. The eval matrix (ticket 12.4) is held to $6 in total, and stops above $0.08 a run; one observed mesocycle was 93k tokens in, 21k out.
