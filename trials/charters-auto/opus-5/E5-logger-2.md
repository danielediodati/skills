# logger charter

The seam: `src/trainer/coach/logger.py` (the graph, its prompt, its question) and
`src/trainer/log.py` (the shape it emits, what it is refused for, what is only flagged).

Input: one report of a workout already performed, in the user's own words; today's date; the prescribed workout that is open (`awaiting`, `prescribed_on`), resolved by the caller; the user's answers to whatever the run asked.
Output: one `PerformedWorkout` -- the deviations only, a provenance on every number, the report verbatim, at most one proposed exclusion -- plus `questions`, `refused` and `confirmed`. The graph writes nothing; the door that asked calls `logger.performed`.

## Free

- Which workout the report is about, `workout_id` included null: which one is *open* is a fact the caller resolves, which one they *trained* is only in the sentence.
- What deviated, and therefore what is in `blocks`: logging is by deviation, and only the reader of the sentence knows what the user did not say. A value nobody gave is left out, never filled in -- writing it marks it `reported`, the one mistake nothing downstream catches.
- Which exercise each name means, inside the prescribed set, by name: a report says *"the bench"* and the prescription is the closed set the user is talking about. The prompt asks for `prescribed_workout` first and `search_exercises` only when nothing prescribed can be what they meant; nothing enforces that order.
- Which tools to call, in what order, and how many turns to spend inside the budget: a substitution needs the catalog and *"did it as prescribed"* needs one read.
- Whether the report determines a value, and so whether to ask: *"4 su 10"* is effort or it is discomfort, and nothing in the sentence says which.
- The wording of each question, one thing in one sentence: the ambiguity is the model's reading, so the question is too.
- Whether a value is `reported` or `asked`: the model is the only witness of whether the number was in the sentence or in an answer.
- Whether `rpe` was volunteered: it is recorded if they said how hard it felt, never asked for and never inferred.
- Whether the report is about pain, and whether that means a movement should stop being prescribed: pain is prose -- no scale, no threshold, nothing accumulates.
- What a proposed exclusion names, its `retest_date` and its `why`: a movement pattern or a loaded joint, never an exercise id and never a dislike. Which of the two it is is not the model's -- the catalog decides.
- `report` is the user's words, verbatim, complete, in their language: a paraphrase is the agent's reading of the user rather than the user. The prompt holds this; no code checks it.

## Constrained

- Six tools, named in `TOOLS`, all reads and no writer: a surface holding tools nobody needs is context paid for on every turn, and a misspelled name is a `SurfaceError` rather than a quietly shorter surface. Anything else asked for comes back as a failed result naming the six.
- What a tool answer shows: trimmed to `KEEPS` -- id, name, equipment, mechanic, primary muscles. `name` is here and not on the planner's list because a report says *"the bench"*.
- The document's shape: strict JSON schema, constrained decoding, no extra fields; `unit` is reps or seconds, `amount` >= 1, `rounds` >= 1, `rest` >= 0 seconds, `rpe` 1-10 or null, `load_kg` >= 0 or null and written with its provenance or not at all, provenance one of three values. A shape that cannot express *"3 rounds of 10 reps of walking"* needs no rule saying so.
- One emission call, and a refused document ends the run: `refused` is an outcome the door states to the user, not an exception and not a turn spent re-emitting. (The planner replans; this does not.)
- `assumed` is never the model's. Adherence fills what the report never mentioned from the prescription and marks it `assumed`, in code (`to_performed`); the validator refuses an `assumed` the prescription contradicts, any `assumed` under no `workout_id`, and an `assumed` load anywhere -- a plan prescribes no load to have assumed one from.
- Which prescribed block a reported one is about: `_paired`, matched by exercise and never by position -- and read by both the validator and adherence, so the answer at the refusal and the answer at the write are one matching read twice.
- Every exercise id exists in the catalog, or the document is refused: an id nobody has is a typo, not a workout. An id that exists and is the wrong exercise is accepted; the prompt's *never write an id you remember* is the only guard.
- What a document may be refused for is a closed list, and every item is about the *document*: nothing performed, an unknown id, a provenance that cannot be true, an unreportable workout, an exclusion naming nothing or expiring before it starts.
- Nothing about the training is ever refused -- it is written and flagged: no prescription behind it, an exercise nobody prescribed, an exercise performed under an exclusion that was in force, a load that moved more than `LOAD_JUMP`. The row saying the user trained through an exclusion is the most valuable one in the database; refusing it would keep the state clean by lying.
- The exclusion's granularity: `exclusions.classify`, against the catalog's own vocabulary, with no granularity field on the wire -- a second answer to the engine's question would file the exclusion under whichever of the two was wrong.
- `retest_date` is required, is `YYYY-MM-DD` by schema and is strictly after `today` by the validator: the column is compared as a string, so *"next week"* sorts after every date there will ever be and the exclusion never expires, with nothing anywhere saying so.
- An exclusion is a proposal: it is classified, shown and confirmed by the user before anything writes it, because an exclusion on `shoulder` takes 251 of 582 exercises out of what may ever be prescribed. A document written by hand (`--from FILE`) is its author's own and stands unasked.
- How a question reaches the user: `ask_user` is an `interrupt()` the graph answers, one question per call, the answer handed back as that call's result -- so it can wait days instead of being a marked line of prose a loop had to recognise (ADR-0004). Open (`clarify`) and closed (`exclusion`) is the graph's to say; each door renders the kind it is given.
- The question budget is kept by taking `ask_user` off the table once three are spent, which is the only bound a model cannot talk its way past; a fourth call inside the turn that spends it is answered with `SPENT_ASKING` and the document is emitted with what is known.
- Nothing in the graph writes, so an interrupted or measured run leaves nothing behind -- and the log eval can put thirty reports through it without leaving thirty performed workouts in the state it measures.
- What the console prints is ASCII: the prompt asks the model for `perche` and `--`, and `cli._ascii` folds whatever comes anyway. `report` is stored verbatim -- presentation only.

## Budget

- Tool calls: 12 (`tools.CALL_BUDGET`), overridable with `--call-budget`. Today's value of a budget, not the line: spent, the reads leave the table and the run goes to `emit` with what it knows.
- Questions: 3 (`ASK_BUDGET`), no override. A bound and not a target -- somebody has just trained and is answering on a phone; a report needing a fourth question is one the agent failed to read.
- Model calls: one per turn, plus exactly one emission. Bounded by the call budget, with LangGraph's default recursion limit as the backstop for a model that only loops.
- Tokens: `max_tokens` 1000 per turn and reasoning `low` (`models.DEFAULT_MAX_TOKENS`, `GROQ_MAX_TOKENS`) -- Groq's free-tier ceiling, today's value and the number to raise first on a paid tier.
- Wall clock: none. A pending question holds on the checkpointer and can be answered days later on the same thread.
