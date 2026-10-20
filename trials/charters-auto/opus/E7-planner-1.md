# planner charter

Input: a `plans.Request` (one workout: equipment, minutes, groups, allocation, exclusions, preferences, refusals, optional `adapting`) or a `plans.MesocycleRequest` (one `Request` per slot, refusals, optional `changing`), assembled by `plans.requested` before the model is called.
Output: a validated `WorkoutPlan` or `Mesocycle`, offered at an `interrupt`; accepted, a prescribed workout (or adapted serving, or kept mesocycle) in SQLite; refused, a new run on the same negotiation; refused by the validator to the end, a run closed `refused`.

## Free
- Which exercises, out of the admissible set: the space is the engine's, the choice of what is good is the agent's (ADR-0001).
- The workout's structure: number of blocks, which exercises share a block, rounds, straight sets vs superset vs circuit (ADR-0001). Nothing in code or prompt says when to reach for which (ticket 11.2).
- Reps or seconds per exercise, and the amount: the `Prescription` shape only forces exactly one unit.
- Rest per block: the prompt's bands (3 min / 90-120 s / 60 s) are a reference, not a rule (ADR-0001, `PLANNING`).
- The reason on every block: the one part only the model can supply; code checks it is non-empty, never what it says.
- How the minutes divide over the groups: the brief's allocation is "a starting point and not an instruction", `allocate` re-divides it and nothing checks the plan followed it (`Request.allocation`).
- How much of the time to use under the cap: today only overrunning is refused (but see Constrained, time window).
- Covering each group with a primary-muscle exercise, and covering each once before a second block: asked in the brief, never validated; measured by the eval's `_does_not_degenerate`, not enforced.
- Proposing a preferred-against exercise anyway, with a `despite` row saying why: proposing it again is the agent's call; doing it silently is not (TRAINER.md invariant 4).
- How a new proposal differs from the ones turned down: the validator takes only the weakest reading, "not the same document" (ADR-0007 item 5).
- What to keep and what to change when adapting today's slot or changing a mesocycle: the brief says "keep what still fits", code checks nothing beyond the usual rules.
- How many cycles a mesocycle runs, and why: the agent's, like a rest (ADR-0008 item 2); code checks only `cycles >= 1` and a non-blank `why`.
- Which tools to call, in what order, and when to stop and emit: within the call budget; a reply with no tool calls goes to `emit`.

## Constrained
- Every `exercise_id` is in `admissible_set` for the request (exclusions, equipment, minutes, groups): held twice, by the emit schema's `enum` and by `_every_id_admissible`, because the set is the space and the model may not widen it (ADR-0001). In a mesocycle the enum is the union over slots; which slot admits which id is the validator's.
- The plan fits the declared minutes, costed by `duration.plan_duration`; one over is refused whole, never trimmed, so the arithmetic error goes back to the agent (ADR-0001).
- The plan lands within `TOLERANCE_MIN = 5` minutes either side of the request, with separate under and over messages: the user's decision in ticket 11.3. Not yet in code, which refuses only a plan over the budget and accepts any plan under it.
- An exercise appears at most once in a plan (`duration.check_plan`); across a mesocycle the same exercise may appear in two workouts.
- The output shape is `WorkoutPlan` / `Mesocycle` under strict structured output (`method="json_schema"`, every property required, `extra="forbid"`): a misspelled field would be a prescription nobody wrote. `Prescription` is unit + amount so both-or-neither cannot be expressed; `rest` is seconds and says so in the schema (an observed `rest: 60000`).
- `despite` names only exercises the user actually said they would rather not do, and every such exercise prescribed has a row: an invented refusal would be printed back to the user as their words; a silent one breaks invariant 4.
- A plan or mesocycle identical to one already turned down is refused: compared whole against the newest refusal, by exercise ids in order against the older ones (ADR-0007 item 4).
- A mesocycle has exactly one workout per slot, in split order, each validated against its own slot's request; a change keeps the count, so `cycles >= changing.cycle`.
- Violations are reported in a fixed order (duplicates, admissibility, then budget only if both passed, then preferences, then refusals) and fed back verbatim through `FEEDBACK`, so the model fixes the plan knowing why.
- A document that is not a plan (bad JSON, wrong shape, an engine block refusal) is a `shape` violation and costs an attempt, never a traceback.
- Standing exclusions and the declared duration cap are folded into a single-workout request before the first turn, once, so the emit schema and the validator read the same space; a time over the cap is refused, never clamped. A mesocycle request is used as `plans.mesocycle_requested` assembled it.
- The tool surface is a named list of ten (`TOOLS`), never derived by subtraction: `prescribed_workout` is out because a planner has no prescription to read back, and a renamed tool must not arrive unnoticed.
- Tool answers are cut to `KEEPS` (`id`, `equipment`, `primary_muscles`): a model shown `name` copied it into `exercise_id`.
- A tool call the model gets wrong (unknown tool, bad arguments) comes back as a failed result it can recover from, not an exception.
- A provider-refused turn is turned into `REFUSED_TURN` and the model is asked again; a spent daily quota is raised at once, since every retry is refused the same way.
- Nothing is written to SQLite before the user accepts: the graph stops at `interrupt`, so the eval, which never resumes, cannot leave phantom prescriptions (ADR-0005).
- Turning a plan down ends the run and starts a fresh one on the same negotiation: messages cleared, brief rewritten with every refusal, a shorter time asked for replaces the budget and drops the allocation (ADR-0007).
- Accepted, a plan is prescribed today, an adaptation is recorded as today's serving of the mesocycle, and a mesocycle is kept with nothing prescribed (ADR-0008 item 4).
- The planning prompts state the rules as rules the model "cannot talk its way around"; the brief carries the user's words only as given (`said`, `because`), never a generated summary (ADR-0007).

## Budget
- Attempts: `ATTEMPTS = 3` emissions per run; past the third refusal the run closes `refused`. Today's value, also quoted to the model in the prompt.
- Tool calls: `tools.CALL_BUDGET = 12` per run, overridable by `--call-budget`; at the budget tools are no longer bound and the model is told to emit with what it knows. A budget, not a rule.
- Provider refusals: `REJECTIONS = 2` in a row, reset by the first accepted turn; the third is raised. Counted in a row so isolated hiccups across validator retries do not end a recovering run.
- Model calls per run: one per planner turn (up to budget + rejections + 1 per attempt) plus one structured `emit` per attempt.
- Reasoning: `models.REASONING = "low"` on every planning model, a trade made for the dev laptop (296 s vs 39 s) and never measured in plans (ticket 11.2).
- Wall time: unbounded in code. Measured: a 5-slot mesocycle change took 585 s on `gpt-oss:20b` (CPU); Groq's free tier refuses it on input tokens (8003 vs 7000 a minute).
