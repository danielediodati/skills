# logger charter

Input: one report in the user's own words, `today`, and the workout `workouts.awaiting` says is open (or none), from `logger.starting`.
Output: a `log.PerformedWorkout` that passed `log.validate` (or a refusal after `ATTEMPTS`), the questions asked with their answers, and whether the user confirmed the proposed exclusion. The graph writes nothing; `logger.performed` does, from the caller.

## Free
- Which workout the report is about: the model may set `workout_id` null against the open one, because only the sentence says the user trained something else.
- Which exercise each named one is: resolved by name inside the prescription, through `search_exercises` when nothing fits, because a report says *"the bench"*, not an id.
- Which blocks to write: only what the user talked about, so a report of "as prescribed" is a document with no blocks.
- Which numbers were said, and what they mean (*serie* are rounds, a bare number is effort or discomfort): reading the sentence is the one job the model exists for (ADR-0009).
- Whether to ask, and what: a question costs the user a reply on a phone, and only the model can tell a word that means two things from a number nobody mentioned.
- Whether a value the prescription is silent on is asked or written as an `assumed` reading: ADR-0009 §2 leaves it to the agent, and the refusal offers both.
- `rpe`: only if the user volunteered it, so it is never a guess.
- Whether pain warrants an exclusion, and which pattern or joint it names: a judgement of the report, not an enum in the schema (ADR-0009 §4).
- Which `retest_date` and what `why`: the eval scores only *after today* and treats `why` as prose.
- Which reads to make, and in what order, among the six tools, within the call budget.
- How to fix a refused document: the refusal comes back as feedback, and the model may read, ask and emit again.

## Constrained
- Tool surface: exactly six reads (`TOOLS`), plus `ask_user` and `done_reading`, and no writer, so an interrupted or measured run leaves nothing behind. Planner tools are absent because they cost context on every turn.
- Tool results are cut to `KEEPS` (`id`, `name`, `equipment`, `mechanic`, `primary_muscles`): what reading a report needs, and `name` because users say names.
- Which workout is open: code resolves `awaiting` and puts it in the brief, because that is a fact, not a judgement.
- Number of questions: at most `ASK_BUDGET` = 3 per report, kept by removing `ask_user` from the tools, the only bound a model cannot talk past. This limits what the user is asked for, not provider spend. Questions past it in the same turn get the fixed `SPENT_ASKING` reply.
- How a question reaches the user: an `interrupt({"kind": "clarify"})` that can wait for days and resumes the same run (ADR-0004), not a marker found in prose.
- The end of reading: `done_reading`, a turn with no tool call, or a spent call budget sends the run to `emit`. Without it, a model that always ends on a tool call sent *"No question needed"* to the user.
- Document shape: one structured-output call against `tools.strict_schema(PerformedWorkout)`, `extra="forbid"`, provenance limited to `reported`/`asked`/`assumed`, `retest_date` required and `YYYY-MM-DD`. A unit or source left next to a null number is dropped, not refused, because refusing it made a local model loop.
- A number the user did not give is null; `log.to_performed` writes the prescribed value as `assumed`, because copying it is the engine's lookup (ADR-0009 §1).
- What gets refused, in `log.validate`: a document reporting nothing, `assumed` with no prescription behind it, an id not in the catalog, a workout that cannot be reported, a null with nothing prescribed to fill it, `assumed` that the prescription does not say, an exclusion `classify` rejects, a retest date not after today. Each one is about the document and never about what the user did; that goes in `flags`, which never refuses.
- Refusal handling: a refusal goes back to the model as `FEEDBACK` with the reason; the catalog's patterns and joints come from the data, never a constant. Up to `ATTEMPTS` = 3 documents per run, and then the run ends `refused` and nothing is written. Every attempt is kept in `refusals`.
- Exclusion granularity: `exclusions.classify` decides pattern or joint from the catalog. The schema has no granularity field, so there are never two answers.
- Exclusion confirmation: a closed yes/no `interrupt({"kind": "exclusion"})` after the document stands. `confirmed` is false until the user says yes, and nothing writes an exclusion before that (ADR-0004). The model is told never to ask about it itself.
- Graph order: logger, tools, emit, validate, then confirm, with an exclusion confirmed only after validation. Every run is closed into the run record (ADR-0007).
- `report` is the user's words verbatim; questions and `why` are in plain ASCII. The prompt asks for both and code does not check either.

## Budget
- Tool calls: `tools.CALL_BUDGET` = 12 reads per run. This is a budget, not a contract: `--call-budget` and `build(budget=)` override it. When it is spent the reads leave the table and the run goes to `emit`. `ask_user` and `done_reading` do not count.
- Questions: 3 per report (`ASK_BUDGET`), a bound and not a target.
- Documents: 3 emits per run (`ATTEMPTS`), each one structured-output call.
- Model calls: one per reading turn plus one per emit. There is no time limit or cost cap in code, so LangGraph's recursion limit is the only outer stop.
