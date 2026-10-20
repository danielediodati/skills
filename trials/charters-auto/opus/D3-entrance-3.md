# entrance charter

Input: a user turn (`heard`: their text, onto the thread's kept `messages` and `said`), or a machine turn (`relayed`: one of `SITUATIONS`).
Output: `answer`, the model's own sentence for the chat; `handoff`, the subgraph the turn reached for or empty; `asked`, the arguments of a checked handoff.

## Free
- Whether a turn is answered here, with a read, or handed on: the entrance is a conversation, not a classifier (ADR-0006 item 1); a router's branches are what it replaced.
- Which handoff a request is: this workout (`adapt_this_workout`), the mesocycle from now on (`change_mesocycle`), or what they declared (`change_declaration`): read from prose the code cannot parse. The prompt gives the cases; the model applies them.
- Asking instead of calling when it cannot tell this workout from "from now on", and asking about an ache or a pain: the prompt asks for this, code does not check it.
- The arguments of `adapt_this_workout` (`minutes`, `equipment`, `leave_out`, `ask_for`, `workout`) and the `said` of the changes: read out of the user's words, which is the entrance's job. They are checked afterwards, not chosen by code.
- Which exercise the user means, looked up with `search_exercises`, and asking them when it cannot place one: names in chat are ambiguous, and an id has to come from the catalog.
- Which engine reads to call and with what arguments: a question about training is answered from them without entering a subgraph (ADR-0006 item 2).
- What is worth remembering: lasting versus true only today. The prompt says "No rule tells the two apart; you do", and the model writes the one-line `conclusion`.
- Every word that reaches the user, after a user turn or after a situation: a constant would be the router again (`RELAYING`, ADR-0006). Italian, one or two sentences, no list: asked by the prompt only.
- Stating no training fact that no tool gave, inventing no exercise, id or date, judging no plan: asked by the prompt (`TALKING`). Code holds only what the model is shown (see Constrained), not what it says.
- How many reads it makes before answering: the prompt says "One call per turn is enough"; code stops it only at the budget.

## Constrained
- The reads on offer are exactly `TOOLS` (8 names); `admissible_set`, `remaining_budget` and `allocate` are left out: they are how a plan is chosen, and the entrance does not plan (ADR-0006 item 4). Named, not derived by subtraction.
- An exercise read comes back with only `KEEPS` (`id`, `name`, `equipment`, `primary_muscles`): the entrance talks in prose, and a name is what it needs.
- The model sees only the system prompt, the user's messages, its own and tool results: a training fact folded in any other way could be stated with no tool behind it (test of that name).
- `TALKING` is prepended on every call, never stored in the history: kept, it would freeze on the day the thread started.
- The handoffs are the closed list `HANDOFFS` (7). `todays_workout`, `plan_mesocycle`, `log_workout` and `set_up` take no arguments; the two changes take only `said`: which workout is due is the rotation's, and a report must reach the logger exactly as typed.
- Which workout is due is read by code (`reading_today` off the mesocycle), never named by the model: the rotation is read off what was performed (ADR-0006 item 4).
- One handoff per turn: the first call wins, any later one is answered `ONE_AT_A_TIME` and not started: two runs from one turn is two drafts for a chat that asked once.
- A turn that has handed off, or that was opened to relay a situation, is bound to no tools: there is nothing left but to speak, and a call there is a second run or answers nobody.
- `adapt_this_workout` and `change_mesocycle` (`CHECKED`) are assembled against the engine before they start: an unknown catalog value goes back as `MISREAD` with the values the catalog has; `TypeError`, `ValueError`, `ExclusionError`, `PlanRejected` go back as `MISREAD` (call again); `plans.Excluded` goes back as `REFUSED` (do not call again); no mesocycle gives `NO_MESOCYCLE`; a machine failure gives `UNREADABLE`. A misread goes back to the model rather than into a plan.
- One string where a list belongs is read as a one-item list; `minutes` and `workout` are cast with `int()`: a lenient reading of a common slip, not a refusal.
- When the next mesocycle is waiting (`prepared`), `plan_mesocycle`, and a `NO_MESOCYCLE` from `todays_workout` or a checked handoff, are replaced by `WAITING_MESOCYCLE` and the handoff `PREPARED`: offering another would plan twice.
- A handoff call is answered with a fixed instruction (`STARTED`, `SERVING`, `NO_MESOCYCLE`, ...), in English, for the model to put into its own words; the model is told it has not seen the result, so it says nothing about what is in it.
- What the machine can ask it to say is the closed list `SITUATIONS` (11), each in ASCII English: a situation that read like a finished sentence would be a constant reaching the user.
- `remember` is offered only with a store, and its `quote` is admitted only if it is in what the user wrote on the thread (case, spacing, typographic quotes and trailing punctuation set aside); an empty `conclusion` is refused. Kept as `provisional`, keyed on its text so a rerun writes it once. Without a user it keeps nothing and says so. Only what they said is kept, never what was inferred.
- Dates are `date.today()`, from code, for requests and conclusions: the prompt forbids the model to invent one.
- `answer` is the last model message's text, stripped. If it is empty the bot says the fixed `FAILED`; a precondition the machine gets wrong is the fixed `BLOCKED`: the two cases where the model is absent or not to be trusted, and where something raised could leak (ADR-0006 item 5).
- The run closes here as `DONE` unless the handoff is in `CARRIED`; `todays_workout` and `PREPARED` end with the entrance's turn, the rest carry the same run on into the subgraph (ADR-0007).
- Nothing here writes or plans, except `remember` to the store: the subgraphs are run by the caller once the turn is answered (ADR-0006 item 6).
- The model is a setting (`ENTRANCE_MODEL`, `ENTRANCE_BACKEND`, `ENTRANCE_REASONING`; default `llama3.1` on Ollama), not code: latency is the lever, and it is per node (ADR-0006 item 3, amended session 12).

## Budget
- Tool calls: `tools.CALL_BUDGET` = 12 per run, shared with the subgraphs, overridable with `--call-budget`: today's value of a budget, not a constraint in itself. Each read counts one, a refused checked handoff counts one; past it the reads and checked handoffs come off the table and any call is answered `SPENT`, refused in `read` as well as unoffered in `talk`. The four unchecked handoffs are never budgeted.
- Model calls: one per round; a user turn is at least two when it calls anything (decide, then say), plus one per read round; a relayed turn is one, with no tools bound.
- Seconds: no cap in code. Measured 0.3-1.2 s a turn on `openai/gpt-oss-120b` via Cerebras, about a minute on `llama3.1` on the dev laptop, 6 s to relay a situation there (ADR-0006).
- Cost and context: no cap in code. The tool definitions are most of the ~2.7k input tokens of a turn.
