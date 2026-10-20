# logger charter

Input: one report in the user's own words, `today`, and the prescribed workout waiting for a report (`awaiting`, `prescribed_on`) or none. The caller looks that workout up with `workouts.awaiting`.
Output: a `log.PerformedWorkout` that has passed `log.validate`, or a run that ends `refused` with no document. The graph writes nothing. The door that started the run writes the document through `logger.performed`, after `log.to_performed` has filled in what the document left out.

## Free
- Which workout the report is about (`workout_id`, or null for training nobody planned): the answer is only in the sentence. The brief says the waiting workout is "almost certainly it" and does not force it.
- Which reads to make, in what order, and when to stop (`done_reading`): reading the sentence is the model's job (ADR-0004). The prompt asks for `prescribed_workout` first, and code does not enforce that order.
- Which exercise the user meant, and the id written for it: matching prose to the prescription's names, or to `search_exercises` for a substitution, is a judgement. The only check is that the id exists in the catalog.
- Which blocks to write: only the ones the user talked about. An empty `blocks` means "done as prescribed", and leaving something out is a decision that adherence then fills in.
- Each number the user gave, and how to read it (rounds vs. amount, *serie* as rounds, rest in seconds): this is reading the sentence. The prompt guides it and the schema bounds it.
- Leaving a number null, and the provenance of a number it writes (`reported`, `asked`, or `assumed` where the prescription is silent): ADR-0009 gives the reading to the agent and the copying to the engine. Code refuses a provenance only when it can be shown false.
- `rpe` and `load_kg`: written only when the user volunteered them. The prompt says never to ask for rpe. Code does not check that the user said it.
- Whether to ask, and the wording of each question: whether a word is ambiguous is a judgement about the report. The prompt asks for one ASCII sentence and no confirming of exclusions. Code checks neither the content nor the ASCII.
- `report`: the model copies the user's words into the document. The prompt says verbatim, and nothing compares it with the input `report`. What gets written is the document's copy.
- Whether to propose an exclusion, and its `value`, `retest_date` and `why`: telling pain from effort or dislike is a judgement. The value is the model's pick, not an enum (ADR-0009). After a refusal, the vocabulary it picks from is read from the catalog.

## Constrained
- The tool surface is six reads, named in `TOOLS`, plus `ask_user` and `done_reading`, and contains no writer. A surface with no write is what lets an interrupted run or an eval run leave the state untouched. Tools this agent does not need would be context paid for on every turn.
- Tool answers are trimmed to `KEEPS` (`id`, `name`, `equipment`, `mechanic`, `primary_muscles`). `name` stays because a report names exercises in words.
- Tool failures, arguments that do not fit and unknown tool names go back to the model as failed results, never as exceptions. An unknown tool name still costs a call.
- The system prompt (`LOGGING`) and the brief are fixed text. The message history is cleared at the start of every run, so a run reads one report and nothing earlier.
- The question budget is `ASK_BUDGET = 3`, enforced by taking `ask_user` off the table. If one turn asks more questions than the budget has left, the extra ones are answered with `SPENT_ASKING`. This limit is a cost to the user, who has just trained and is on a phone. When it runs out, the asking stops and the document is still emitted.
- A clarifying question is an `interrupt` of kind `clarify`, and the user's answer goes back verbatim as the tool result. A question can wait days, and it is a call rather than a marker in prose that the loop has to spot (ADR-0004).
- The document is asked for once per attempt, in a separate `emit` turn, with strict `json_schema` structured output and no tools. Constrained decoding makes the shape conform by construction.
- Parts of the shape are fixed in code. Extra fields are forbidden. Each number goes with its provenance, both or neither. A unit or provenance next to a null number is dropped rather than refused, because refusing it looped a local model. `rpe` is 1-10. `retest_date` is `YYYY-MM-DD`, because a non-date sorts as never expiring.
- `log.validate` refuses only statements about the document, never about what the user did: no blocks and no workout; `assumed` with no prescription; an id not in the catalog; a workout that cannot be reported; a null that no prescription fills; an `assumed` value the prescription contradicts; any `assumed` load; an exclusion that `classify` rejects or that is not re-tested after today. A fact is flagged, never refused (`log.py`).
- A refusal of either kind, shape or validator, goes back to the model as `FEEDBACK` and the run tries again, up to `ATTEMPTS = 3` documents. After the third refusal the run ends `refused`, nothing is written, and the chat says it was not logged. Feedback is ADR-0009's answer, in place of more rules in code. The 3 copies the planner's loop, and no reason is given for the number itself.
- `exclusions.classify` decides an exclusion's granularity (pattern or joint) against the catalog. No granularity field exists on the wire. A second answer to that question would be filed under whichever of the two was wrong.
- The user confirms a proposed exclusion with a closed yes/no `interrupt` (kind `exclusion`), never the model. The question shows the model's `why` alongside the value `classify` gave. If the user declines, the workout is still written without the exclusion. Nothing writes an exclusion until the user says so (ADR-0004).
- `log.to_performed` fills every gap with the prescribed value, marked `assumed`, matching blocks by exercise and never by position. Copying a prescribed number is a lookup, and lookups belong to the engine (ADR-0009).
- `today` and the waiting workout come from the caller. Which workout is open is a fact, not a judgement.

## Budget
- Tool reads: `tools.CALL_BUDGET = 12` per run, shared across attempts. This is today's value of a budget and can be raised with `--call-budget`. It is enforced by taking the reads off the table and sending the run to `emit`. One turn can run past it, because every call already in that turn is executed.
- Questions: at most 3 per run. This is the constraint itself, a cost to the user, not a value waiting to be raised.
- Documents: at most 3 `emit` calls per run (`ATTEMPTS`). The code does not say whether this is a fixed limit or a value that may be raised.
- Model calls: one per reading turn, plus one per `emit`. The total has no explicit cap beyond the bounds above. `ask_user` and `done_reading` cost no read. The backstop is LangGraph's default recursion limit, because no caller sets one.
- Tokens: on Groq, each turn is capped at `GROQ_MAX_TOKENS`, default 1000, with reasoning included (`REASONING = "low"`). The 1000 comes from the free tier and is the first number to raise on a paid one.
- Time: no limit. A run held on a question or a confirmation waits as long as the user does.
