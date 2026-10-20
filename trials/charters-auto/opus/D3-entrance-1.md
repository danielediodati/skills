# entrance charter

Input: one turn on a thread. Either what the user wrote (`heard`), appended to the thread's kept conversation, or one situation the machine names (`relayed`), such as a plan kept or a report logged.
Output: `answer`, the model's own sentence for the chat, plus `handoff` (which subgraph, if any, the caller starts next) and `asked` (the arguments of a checked handoff).

## Free
- What a user turn needs: answer directly, call a read, or hand off to one of the seven handoffs. The prompt gives the cases, code checks none of them. A router with fixed branches is what ADR-0006 replaced.
- This workout, the mesocycle, or what they declared, and when to ask instead of calling (*«niente panca»*). Only the model reads intent from prose, and the prompt tells it to ask rather than guess.
- An ache, or a dislike with nothing asked for, starts nothing, and the model may ask one question about it. The prompt asks for this, code does not enforce it.
- The fields of `adapt_this_workout`: `minutes`, `equipment`, `leave_out`, `ask_for`, `workout`, and `said` in the user's words. Turning *«a corpo libero»* into `["body only"]` is reading, and code checks the result (see Constrained).
- Which reads to call, and with which arguments: answering a training question is judgement. The facts themselves come from the tools.
- Whether something said is lasting enough to `remember` (*«la cyclette mi annoia»*), and the one-line conclusion drawn from it. The prompt says no rule tells this apart from *«oggi sono distrutto»*.
- The words of every reply, including how it relays a situation or a handoff's result. These are the whole point of ADR-0006: a situation whose words are fixed is a constant by another name.
- The reply is Italian, one or two sentences, never a list. The prompt asks for this, but code checks neither the language nor the length.
- How it recovers from a refusal that says `MISREAD`: it can call again with the error put right, or ask the user.

## Constrained
- Which handoffs and reads exist: closed lists, `HANDOFFS` (7) and `TOOLS` (8 engine reads), plus `remember` only when a store is given. `admissible_set`, `remaining_budget` and `allocate` are left out because they are planning, and the entrance does not plan (ADR-0006 item 4).
- Every tool is read-only. Nothing in the node writes or plans. Subgraphs are started by the caller after the turn is answered (ADR-0006 item 6).
- `todays_workout`, `plan_mesocycle`, `log_workout` and `set_up` take no arguments. Which workout is due belongs to the rotation, and a report reaches the logger exactly as typed. A parameter would be a place to invent one. Tested.
- `change_mesocycle` and `change_declaration` take only `said`. `adapt_this_workout` requires `said`, and the field it names a workout with is `workout`, a cycle number the user asked for, never the one that is due. Tested.
- Which workout is due, and what is in it: read by code (`reading_today`). The model is told only `SERVING`, `NO_MESOCYCLE` or `UNREADABLE`, never the workout. The workout is sent by the bot after the reply, with no model call.
- `adapt_this_workout` and `change_mesocycle` are assembled into a planner request before they start (`CHECKED`). An unknown catalog value, an exclusion error, a rejected plan, or a `TypeError`/`ValueError` goes back as `MISREAD` with what to fix. The catalog's valid values are listed, read from the data. An excluded exercise comes back as `REFUSED` and is not to be retried. A misread is caught before a planner run of minutes is spent on it.
- One handoff per turn: the first handoff call wins, and any later one is answered `ONE_AT_A_TIME`. Two runs from one ask would mean two drafts and two plans. Tested.
- After a handoff, and on a relayed turn, no tools are bound: the next model call can only speak. A tool call there would start a second run, or answer nobody. Tested.
- When the next mesocycle is already waiting or being prepared, `todays_workout`, `plan_mesocycle`, or a check returning `NO_MESOCYCLE` becomes `PREPARED` with `WAITING_MESOCYCLE`, so the user is not offered a second one.
- A handoff call is answered with a fixed instruction for the model (`STARTED`, `MISREAD`, `REFUSED`, `SPENT`, `ONE_AT_A_TIME`, `WAITING_MESOCYCLE`), never with words meant for the user. What reaches the chat is still the model's sentence.
- `remember` keeps a conclusion only if `quote` appears word for word in one of the user's messages on the thread, and `conclusion` is not empty. Otherwise the call is refused and the model is told why. It is stored as provisional, dated today, and keyed on its content so it is written once. Never remember what was inferred (ADR-0009).
- What the model is shown: the system prompt, prepended fresh on every call and never stored, then the conversation, then tool results. No brief, and no training fact folded into a prompt. This is where *no training fact a tool did not give* is kept (ADR-0006 item 4). Tested.
- Exercise reads come back trimmed to `KEEPS`: `id`, `name`, `equipment`, `primary_muscles`. The entrance talks in names, not ids.
- The conversation (`messages`, `said`) outlives every run on the thread, and every other field is cleared when a run starts. The entrance is the only node that remembers the turn before.
- The situations the machine can name are the closed list `SITUATIONS` (11). Each is an instruction, not a line to quote. Tested.
- A reply with no words, or a turn that raised, reaches the chat as the bot's fixed `FAILED`, and the error goes to the log. `BLOCKED` and `FAILED` stay constants because the model is absent or not to be trusted there (ADR-0006 item 5).
- The entrance is not reached at all while nothing is declared. The bot sends every message to the interview instead (ADR-0013).
- Dates on requests and conclusions are `date.today()`, never the model's. The prompt also forbids inventing an exercise, an id or a date.
- The model: `ENTRANCE_MODEL`, `ENTRANCE_BACKEND` and `ENTRANCE_HOST` are settings. On OpenRouter the default is `openai/gpt-oss-120b` at low effort on Cerebras, with the host pinned and no fallback, so the run record names one host (ADR-0011). It was chosen for latency, because this is the node the user waits on. There is no suite and no bar yet.

## Budget
- Tool calls: `tools.CALL_BUDGET` = 12 per run, overridable with `--call-budget`. That is today's value of a budget, not a constraint in itself. It counts reads, `remember`, and refused checked handoffs. A checked handoff that starts, and the four unchecked handoffs, do not count.
- Past the budget, reads, `remember` and checked handoffs are no longer offered, and if called anyway they are answered `SPENT` and not run. This is held twice, in `talk` (not offered) and in `read`/`hand_off` (not run). The unchecked handoffs stay offered, so the user's request can still go through. Tested.
- Model calls: no cap of their own. A user turn is about budget + 2 at most, bounded otherwise only by LangGraph's recursion limit. A relayed turn is one call.
- Context: the conversation is never trimmed. Every call reads the whole thread plus the tool definitions, about 2.7k tokens for the tools alone (ADR-0006).
- Cost and time, measured, not enforced: $0.001–0.002 and 0.3–1.2 s per turn on the default configuration (ADR-0011).
