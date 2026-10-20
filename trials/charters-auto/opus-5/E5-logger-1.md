# logger charter

The seam is `coach/logger.py` (the graph, its prompt and its one extra tool) over `log.py` (the shape it emits and the little it is refused for).

Input: one report in the user's own words, `today`, and the prescribed workout the caller resolved as open (`awaiting`, `prescribed_on`) or nothing; six read tools over the engine.
Output: a `PerformedWorkout` document — which workout it reports against, the blocks that deviated with a provenance on every number, the user's words, at most one proposed exclusion — plus the questions it asked, the validator's refusal or none, and whether the user confirmed the exclusion. The graph writes nothing.

## Free

- **Which workout the report is about**: the brief names the open one and says it is almost certainly it, and the model may still emit `workout_id: null` — a user who trained something else says so in the sentence, and that sentence is the only place the answer is.
- **Which exercise each phrase names**, resolved by name inside the prescribed workout: *"la panca"* against a closed set of four is reading, not search, and no code can do it.
- **When a phrase is a substitution**, meaning nothing in the prescribed set can be what they meant, and therefore when `search_exercises` is called at all: deciding that is the whole judgement, and it is the interesting case.
- **What counts as a deviation worth emitting**, and so what is left out for adherence to fill in: logging by deviation only works if the model decides what differed.
- **Whether *serie* is rounds or reps**, and which number is the `amount`: the prompt states the rule, nothing in the shape can tell a wrong round count from a right one.
- **Whether the sentence determines a value or needs a question**, and which value: *"4 su 10"* is effort or discomfort, and only the reader of the sentence can say it is neither.
- **What to ask, how to word it, and in what order**: one question put to somebody on a phone who has just trained; a fixed question would be a question about a report nobody read.
- **Whether the report is about pain at all**, and so whether to propose an exclusion, which movement or joint it names, which day to re-test, and the `why`: pain is prose, with no scale and no threshold, and the engine refuses to hold an opinion about it (ADR-0001).
- **Whether the user volunteered an rpe**: it is recorded only if they said how hard it felt. The prompt says never ask for it and never infer it; the shape only removes the provenance that would dress an invented one as asked.
- **Which tools to call, in what order, and when to stop reading and emit**: the budget bounds it, nothing prescribes it.
- **`report` is the user's own words, verbatim, untranslated**: a paraphrase is the agent's reading of the user rather than the user, and a hypothesis is formed off this field. Asked by the prompt and left to the model — code checks only that it is non-empty, and the log eval is the only thing that scores it word for word.
- **An id is read from a tool result and never remembered**: an id that does not exist is refused, but one that exists and is the wrong exercise files the training under something nobody did and nothing anywhere says so. The prompt carries this rule; code cannot hold it, and that is the trade made for showing the model exercise names at all.
- **The question and the `why` are written in plain ASCII**: they are printed to a Windows console. The prompt asks; the CLI transliterates what it can at print time. Never applied to `report`.

## Constrained

- **Six tools, named in `TOOLS`, all reads**: a writer on the table means the model decides when the database changes. Named rather than derived by subtraction, and a tool asked for and not offered comes back as a result listing what it does have, not as a crash.
- **Nothing the graph does writes.** `logger.performed` is the one writer and the door that asked calls it, after the document stands — which is what lets an interrupted run, and thirty eval runs, leave nothing behind.
- **The document is emitted as a strict JSON schema derived from `PerformedWorkout`**, extras forbidden: the shape is one definition, and prose would have to be parsed back into it.
- **The provenance vocabulary is three values** — `reported`, `asked`, `assumed` — fixed as a `Literal` so a fourth is a shape error, not a CHECK violation nobody can read.
- **`assumed` is the engine's and is refused to the model where it can be shown false**: with no prescription behind the workout at all, where it contradicts the prescribed number, and on a load anywhere (a plan prescribes none). Where the prescription is silent it stands — only what can be shown false is refused. The one mistake nothing downstream can catch is a number the user never gave marked `reported`, and this is the half of it code can see.
- **A load and its provenance stand or fall together**, and `load_kg >= 0`: a provenance describing nothing is not a provenance (migration 0006's own rule).
- **The numeric bounds are the schema's**: `amount >= 1`, `rounds >= 1`, `rest >= 0` seconds, `rpe` 1-10, `unit` is `reps` or `seconds`. They exclude what cannot be meant, not what is unlikely.
- **Every exercise id must be in the catalog**: an id nobody has is a typo, and the write would refuse it a moment later as a foreign key naming a column.
- **A report is never refused for what the user did.** Every refusal is about the document; everything about the training is a `Flag` — no prescription, a substitution, an exercise performed under a standing exclusion, a load that moved further than `LOAD_JUMP`. A row the user trained straight through an exclusion is the most valuable row there is.
- **`LOAD_JUMP` is 0.2, and it flags rather than refuses**: a fifth is far outside what progression produces and comfortably inside the mistakes it catches (pounds typed as kilos). A written rule, raisable, and never a refusal.
- **Adherence is code's**: what the document leaves out is filled from the prescription by `log.to_performed`, matched by exercise and never by position. The model never restates the unchanged parts, and the flags are read off the filled blocks rather than off the document.
- **The exclusion's granularity is never the model's** — there is no such field on the wire. `exclusions.classify` decides pattern or joint against the catalog's own vocabulary; a second answer on the wire would file the exclusion under whichever of the two was wrong.
- **`retest_date` is required, is `YYYY-MM-DD`, and must be strictly after `today`**: the column is compared as a string, so *"next week"* sorts after every date there will ever be and the exclusion never expires — a wall with no way back, which TRAINER.md calls the one failure this state cannot afford. Which day it is stays free.
- **No exclusion is written without the user confirming it**, as a closed interrupt the graph routes to structurally — the model does not choose whether it is asked. An exclusion on `shoulder` takes 251 of 582 exercises out of what may ever be prescribed; the CLI defaults the answer to no. A document given with `--from` is exempt: the author's own proposal stands unasked.
- **A question is a tool call the graph answers with `interrupt()`**, never a marked line in prose: nothing reads the model's prose, and the run can wait days for the answer on the same thread.
- **`ask_user` takes exactly one required argument**, a question, and is never on the engine's surface: a tool the engine served would be the engine talking to the user.
- **Which prescribed workout is open is resolved by the caller**, not asked of the model: which workout is awaiting a report is a fact.
- **Tool results are trimmed to `KEEPS`** — id, name, equipment, mechanic, primary muscles. `name` is here and not on the planner's list because a report says *"the bench"*; everything else is context paid for on every turn.
- **A refusal ends the run.** There is no repair turn: the document is recorded as refused, the run document says `REFUSED`, and the door reports the sentence. The model is not given a second attempt at the same report.

## Budget

- **Tool calls: 12** (`tools.CALL_BUDGET`, `--call-budget` overrides). Today's value of a budget, not the constraint: a spent budget takes the reads off the table and routes the run to `emit` with what it knows.
- **Questions: 3** (`ASK_BUDGET`). A bound and not a target, and a hard one — kept by removing `ask_user` from the table, because a budget answered with a sentence is one a model can talk past. The turn that spends it has its extra questions answered with `SPENT_ASKING` rather than reaching the user.
- **Model calls: one per turn, plus exactly one structured emit call.** No retry on a bad emission.
- **Output: `max_tokens` per turn, 1000 by default** (`GROQ_MAX_TOKENS`), shared with the model's reasoning.
- **Measured by `trainer eval --suite log`**: thirty reports, three repetitions each, scored by code and never by another model. Eighteen on document equality and the volume it produces, twelve on one bit — did it ask — with false confidence weighted double.
