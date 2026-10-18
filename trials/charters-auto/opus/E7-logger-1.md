# logger charter

Input: one report in the user's own words, today's date, and the prescribed workout still waiting for a report (id and date, or none), resolved by the caller.
Output: a `log.PerformedWorkout` that `log.validate` accepted, or a run ended `refused`; the questions asked with their answers; whether the user confirmed the proposed exclusion. Nothing is written by the graph.

## Free
- Which workout the report is about: the brief names the waiting one as "almost certainly it", but the model may emit `workout_id` null, because only the sentence says whether the user trained something else.
- Which exercise a phrase means: resolved by name inside the prescribed set, else through `search_exercises`; reading "the bench" is the job the model is there for (ADR-0001, ADR-0004). The prompt says "never an id you remember", and `validate` refuses ids the catalog does not have.
- Which blocks to write: only what the user talked about; a report of a workout that went as prescribed has no blocks, since logging is by deviation.
- Each number the user gave, and its unit: whether a bare number is effort or discomfort, and whether "sets"/"serie" means rounds or amount (the prompt says rounds). Only the model can read the sentence.
- Whether to ask, what to ask and how to word it: only about something the user *said*, one thing per call; a number the user did not mention goes in as null. The prompt asks for one sentence in plain ASCII, and no code checks either.
- Ask, or write a reading, where the prescription is silent (a substitute's rest): the model's call, ADR-0009 §2.
- Whether the report calls for an exclusion, and its value (a pattern or a joint), `retest_date` and `why`: a reading of pain as opposed to effort or dislike. The vocabulary comes from the catalog (ADR-0009 §4), not an enum, and the user confirms it. The prompt asks for `why` in ASCII; no code checks it.
- `rpe`: only if the user said how hard it felt. The prompt says never ask for it, and `ask_user` cannot carry a value into it without the user offering one.
- `report`: the user's words verbatim and complete, in their language. The prompt holds this; code checks only that it is not empty.
- Which reads to make, in what order, and when to stop (`done_reading`). The prompt says `prescribed_workout` comes first; code does not enforce the order.
- How to fix a refused document: the refusal goes back as prose, and the model may read, ask and emit again ("feedback, not more rules in code", ADR-0009).

## Constrained
- Tool surface: the six reads in `TOOLS`, named rather than derived, plus `ask_user` and `done_reading`. There is no writer, and a tool that is not offered (including a planner tool) comes back as a failed result. Leaner context every turn, and a run that cannot write.
- Tool results are trimmed to `KEEPS` (`id`, `name`, `equipment`, `mechanic`, `primary_muscles`), with `name` kept because reports name exercises.
- Nothing in the graph writes. `performed()` is the one writer, called by the door that asked, so an interrupted or measured run leaves no rows behind.
- An exclusion is written only when `confirmed`. Code asks for confirmation through a closed yes/no `interrupt` after emit, with the granularity taken from `exclusions.classify` and never from the model. The prompt forbids asking it in the conversation (ADR-0004).
- Question budget `ASK_BUDGET = 3`, enforced by taking `ask_user` off the table once spent. Questions past the budget that the same turn already sent get `SPENT_ASKING`. A model cannot talk its way past a missing tool. The number is a bound and not a target: the user has just trained and answers on a phone.
- A question is an `interrupt` that can wait for days, and resuming replays the node's reads, which is safe only because every tool on the surface is a read. The answer is taken as `str`, and the confirmation as `bool`.
- `questions` is recorded as a state field, not read back from prose, because the log eval scores "did it ask" on it.
- Emit is one structured-output call (`json_schema`, strict schema of `PerformedWorkout`) per attempt, sent with the fixed `EMIT_LOG` line.
- Shape, fixed by schema: provenance is exactly `reported`/`assumed`/`asked`; numbers ≥ 1 (rest ≥ 0, load ≥ 0, rpe 1-10); a number and its source go together, and companions of a null number are dropped instead of refused. `retest_date` is required and written `YYYY-MM-DD`; there is no granularity field; extra keys are forbidden.
- `validate` refuses only statements about the document: nothing performed and no workout; `assumed` with no prescription, or `assumed` the prescription contradicts; an id the catalog does not have; a workout that cannot be reported; a value left out that nothing prescribes; an exclusion `classify` rejects; a `retest_date` not after today. What the user actually did is flagged and never refused.
- A number left null is filled with the prescribed one, marked `assumed`, by `log.to_performed`. Copying from the prescription is a lookup, and lookups belong to the engine (ADR-0009 §1).
- Refusal loop: `ATTEMPTS = 3` documents per run, each refusal sent back with the fixed `FEEDBACK` text. After the third the run ends `refused`, and `refusals` keeps every attempt for the record.
- A model turn with no tool calls goes straight to emit; `done_reading` exists so that a model which ends every turn on a tool call is not left with `ask_user` as its only way to end.
- Every run starts from cleared messages, with the fixed `LOGGING` system prompt and a `brief` built by code.

## Budget
- Read calls: `tools.CALL_BUDGET = 12` per run by default, a budget `--call-budget` / `build(budget=)` can raise. Once it is spent the run goes to emit with what it knows. It is not reset between attempts.
- Questions: 3 per run (above). That is the constraint itself, not a value waiting to be raised.
- Emits: at most 3 per run.
- Model turns have no cap of their own: reads, questions and attempts bound them, and LangGraph's recursion limit is the backstop.
- Seconds and cost: no limit in code. `timings` records each node.
