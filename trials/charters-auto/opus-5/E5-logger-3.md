# logger charter

The seam is `coach/logger.py` — the graph that reads one report of a workout that has already happened — together with `log.py`, the shape it has to emit into and the refusals that shape carries.

Input: one report in the user's own words, today's date, and the prescribed workout that is open (id and date, resolved by the caller, or the statement that none is).
Output: one `PerformedWorkout` document, the questions it asked with the answers it got, whether a proposed exclusion was confirmed, and `refused` when the document did not stand. Nothing is written by the graph.

## Free

- Which workout the report is about, including `null`: a user who trained something nobody planned says so in the sentence, and the sentence is the only place that answer is. The brief names the open workout as *almost certainly it*; it does not decide it.
- Which exercise each name in the report is: resolution is against the prescribed set, and a name matched to an id is a reading of prose no code can do.
- Whether something is a substitution — nothing in the prescribed set can be what they meant — and therefore whether `search_exercises` is called at all.
- Which values deviated and which are left out: logging is by deviation, so what the document omits is the model's claim that it went as prescribed. A workout done as asked is a document with no blocks.
- Whether the report determines a value or has to be asked about: *"4 out of 10"* is effort or it is discomfort, and only the reader of the sentence can tell that it is neither.
- The wording of each question, and which one is worth the budget: one thing in one sentence, to somebody answering on a phone.
- Whether the report is about pain at all, and whether what they said means a movement should stop being prescribed for a while.
- The exclusion's `value`, `retest_date` and `why`: what movement or joint is implicated, how long is enough, and which sentence this is a reading of.
- Which tools to call and in what order, within the budget. The prompt asks for `prescribed_workout` first because it is the closed set everything else resolves inside; nothing enforces the order.
- Whether an id it writes is the *right* exercise: code checks only that the id exists. An id that exists and is the wrong exercise files the training under something the user did not do, and nothing downstream says so — which is why the prompt forbids writing a remembered id.
- `report` is the user's words verbatim, in their language, not a summary and not a translation: it is what a hypothesis is later formed from, and a paraphrase is the agent's reading rather than the user. Prompt only; no code compares it with the input.
- Leaving a value out rather than filling it in. Prompt only, and the prompt says so: writing it marks it `reported`, which is the state claiming the user said it, and that is the one mistake here nothing downstream can catch.
- Reading *sets* and *serie* as `rounds` and never as `amount`. Prompt only — both are legal integers, so a misread is a document that validates.

## Constrained

- The tool surface is six named reads (`prescribed_workout`, `unreported_workouts`, `last_performed_load`, `pattern_history`, `search_exercises`, `compare_variants`), listed rather than derived by subtraction: the planner's arithmetic tools are not questions about the sentence in front of this agent, and a surface nobody needs is context paid for on every turn.
- No tool writes, and the graph never writes: `logger.performed` is reached from the door that asked, after the user has seen the document. That is what makes an interrupted run leave nothing behind and lets the eval put thirty reports through the graph.
- A tool the model was not offered comes back as a failed tool result naming the ones it has, never as an exception: its mistake, and one it can recover from in the next turn.
- Tool answers are trimmed to `id`, `name`, `equipment`, `mechanic`, `primary_muscles`. `name` is here and not on the planner's list because a report says *"the bench"*.
- Asking is an `interrupt()` and not a marked line in prose: the question goes to whoever wrote the report and the answer comes back as the tool's result, so a run can wait days (ADR-0004).
- The user's answer reaches the model verbatim, as the result of the call. Nothing summarises or validates it.
- At most `ASK_BUDGET = 3` questions per report. Kept by taking `ask_user` off the table on the next turn — the only bound a model cannot talk its way past — and a call that spends the budget within a turn is answered with `SPENT_ASKING`. A bound, not a target: running out stops the asking and the document is emitted with what is known. Tighter than the call budget: a constant with no CLI override, on the ground that a fourth question is a report the agent failed to read.
- The call budget is `tools.CALL_BUDGET = 12`, overridable per run with `--call-budget`. Today's value of a bound, not the constraint itself: when it is spent the tools come off the table and the run goes straight to `emit`.
- Exactly one emit call, with `PerformedWorkout` as a strict JSON schema (every property required, no extras), and no repair turn: a document that does not parse or does not validate ends the run as `refused`, and the model is never shown the refusal to try again.
- A refusal is an outcome in the state, never an exception about the user: every refusal is about the document — a typo, a provenance that cannot be true, an exclusion naming nothing. A report is a fact and is never refused for what the user did.
- Everything that can be said about the *training* is a `Flag`, computed in code off the blocks that will be written: no prescription behind it, an exercise nobody prescribed, a movement performed under a standing exclusion, a load that moved more than `LOAD_JUMP = 0.2` from the last one recorded. Flags are never the model's to write and never refuse a row.
- The gaps are filled by `to_performed`, not by the model: a prescribed exercise the document never names comes through with the prescription's own numbers and a provenance of `assumed`, matched by exercise and never by position.
- `assumed` is the engine's provenance and the model may not claim it where it can be shown false: no prescription behind the workout at all, a value the prescription contradicts, or any load — a plan prescribes none, so there is nothing a load could have been assumed from. Where the prescription is silent (a substituted exercise, a block nobody prescribed) `assumed` stands.
- The three provenances are a closed `Literal` (`reported`, `assumed`, `asked`); a fourth is refused in the shape error, before the database refuses it as a constraint nobody can read.
- `load_kg` and `load_kg_source` are written together or both left empty, and zero is a claim that the bar was empty rather than *no load*. A provenance describing nothing is not a provenance.
- `rpe` is null unless the user volunteered it, carries no provenance field at all, and is never asked for: with no `_source` column, `asked` and `assumed` cannot arise for it.
- Units are `reps` or `seconds` and travel with one amount; `amount >= 1`, `rounds >= 1`, `rest >= 0` in seconds, `rpe` within 1–10. A shape that cannot express *"3 rounds of 10 reps of walking"* needs no rule saying so.
- `blocks` may be empty and `workout_id` may be null, but not both: a report that says nothing was done and names no prescription is a report of nothing.
- Every exercise id must be in the catalog, and the workout it reports against must exist and not already have been reported (`workouts.reportable`), both checked before anything is rendered.
- The exclusion's granularity is the catalog's answer, never the model's: `ProposedExclusion` has no granularity field, and `exclusions.classify` decides pattern or joint against the catalog's own vocabulary. A granularity on the wire would be a second answer to a question the engine already answers.
- `retest_date` is required and is checked to be `YYYY-MM-DD` by `strptime`, because the column is compared with `>` and *"next week"* sorts after every date there will ever be — a wall with no way back that nobody had to decide to build. It must also be after `today`, which `validate` holds and the schema cannot.
- A proposed exclusion is a proposal: the user is shown it — classified, so the question says what is actually being stopped — and nothing is written before they confirm. `confirmed` is `False` until they say so. An exclusion on `shoulder` takes 251 of 582 exercises out of what may ever be prescribed.
- `trainer log --from FILE` skips the confirmation: the author's own proposal stands unasked, because the confirmation exists for an exclusion a *model* read out of a passing remark.
- Which prescribed workout is open is the caller's, not the model's: that is a fact, and only *which workout the report is about* is a judgement.
- Prose the model writes — the question, and an exclusion's `why` — is plain ASCII, because it is printed to a Windows console; the CLI transliterates what slips through. This never touches `report`, which is copied exactly as the user typed it.
- The run is recorded either way — the calls, the questions, the document, the timings, and the ending `DONE` or `REFUSED` — because the refused run is exactly the one you open to find out what the model did.

## Budget

- Tool calls: 12 per run (`tools.CALL_BUDGET`, `--call-budget`), after which the tools come off the table and the document is asked for anyway.
- Questions: 3 per report (`ASK_BUDGET`), no override.
- Model calls: one per turn, plus exactly one for the document. No judge, no critic, no retry; LangGraph's recursion limit is the backstop, not the bound.
- Tokens: on Groq, `max_tokens` per completion — 1000 by default (`models.DEFAULT_MAX_TOKENS`), with the reasoning inside it; on Ollama, the context `OLLAMA_CONTEXT_LENGTH` declares, which must be at least 8192.
- Wall clock: none. A pending question is an interrupt against a checkpoint and may be answered days later on the same run.
