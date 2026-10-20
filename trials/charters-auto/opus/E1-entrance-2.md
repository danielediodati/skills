# entrance charter

Input: one turn: what the user wrote (`heard`, appended to the thread's kept `messages`) or one situation the machine names (`relayed`, one of `SITUATIONS`).
Output: `answer`, the model's sentence for the chat, and `handoff`, which subgraph the turn reached for (empty when it answered itself).

## Free
- What to do with a user turn (answer, read, or which handoff): the model reads prose; a router's fixed branches are what ADR-0006 replaced.
- Every word the user reads, including for each of `SITUATIONS`: a branch whose words are written in advance is the router this replaced. The situation text is an instruction, never shown.
- Which reads to call, with which arguments, and how many in one turn (within the budget): questions about training are not foreseeable.
- Language, length and tone (Italian, one or two sentences, no lists): asked by `TALKING`/`RELAYING`, checked by no code.
- Stating no training fact no tool gave, not deciding which workout is due, not judging a plan, inventing no exercise, id or date: asked by `TALKING` (ADR-0006 item 4); code enforces it only through what the model is shown and what the handoffs take (below).
- Relaying no numbers and no exercise names: asked by `RELAYING`, unchecked.

## Constrained
- The model's context is `TALKING`, the thread's messages, the relayed situation and tool results, nothing else: a training fact folded in any other way could be stated without a tool having said it (test-held).
- `TALKING` is prepended each run, never stored in history: stored, the prompt would be frozen at the day the thread started.
- The reads are the closed list `TOOLS`, named, never derived: `admissible_set`, `remaining_budget`, `allocate` are planning arithmetic and the entrance does not plan.
- Every tool is read-only; nothing in the entrance writes or plans: writes and plans belong to the subgraphs (ADR-0006 item 6).
- Exercise records reaching the model are cut to `KEEPS` (`id`, `name`, `equipment`, `primary_muscles`): it answers in prose and needs `name`.
- The handoffs are the closed list `todays_workout`, `plan_mesocycle`, `log_workout`, and take no arguments: which workout is due and what the report says are not the entrance's to name; the logger gets the user's text verbatim.
- One handoff per turn; a second in the same turn is not started and is answered `ONE_AT_A_TIME`, the first call wins: two runs from one ask are two drafts.
- After a handoff, and on a relayed turn, the model is called with no tools bound: a tool call there is a second run nobody asked for, or one answering nobody.
- Every tool call in a turn gets a `ToolMessage`, including reads beside a handoff: an unanswered call is a history the next turn is refused on.
- Which workout is due and whether one exists is read by code (`reading_today`), answered as `SERVING`, `NO_MESOCYCLE` or `UNREADABLE`; the workout itself is sent by the bot, with no model call: the rotation decides, not the model.
- A machine failure behind `todays_workout` is `UNREADABLE`, distinct from no mesocycle: a broken database must not read as an empty one.
- What a handoff call returns is a fixed instruction (`STARTED`), never words for the user: the model finds its own.
- A read the model got wrong comes back as a failed `ToolMessage` the model sees; any other exception propagates.
- An empty answer, or a turn that raised, reaches the chat as the bot's fixed `FAILED`, never a generated line: nothing raised leaves the machine (ADR-0006 item 5). `BLOCKED` is fixed too.
- `SITUATIONS` is the closed list of what the machine can ask the entrance to say: a test puts each one to the model.
- The run closes in `answer` unless the handoff is `plan_mesocycle` or `log_workout`, which carry the same run on: the user asked once, so it is one run (ADR-0007).
- The model is the entrance's own (`ENTRANCE_MODEL`/`ENTRANCE_BACKEND`, default `llama3.1` on Ollama, no reasoning phase): this is the node the user waits on. A setting, not code.

## Budget
- Reads: `tools.CALL_BUDGET` = 12 per run, overridable by `--call-budget`; today's value of a budget, not the constraint itself. Once spent, reads are no longer offered (`talk`) and any read called anyway is answered `SPENT`, not run (`read`). Reads called beside a handoff run without a budget check.
- Model calls: no cap of their own; bounded by the read budget plus one per handoff, and past that only by LangGraph's recursion limit. The prompt's *one call per turn is enough* is not held by code.
- Latency: about a minute per user turn on `llama3.1` on CPU (≈2.7k input tokens, mostly tool definitions, two model calls); about 6 s for a relayed turn, which binds no tools (ADR-0006). Not enforced; levers are the model settings.
