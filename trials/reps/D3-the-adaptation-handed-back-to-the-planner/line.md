# D3 - the line a replay is judged on

Seams: entrance (`src/trainer/coach/entrance.py`); planner (`src/trainer/coach/planner.py`, `src/trainer/plan.py`)

Where the code has it at the parent: ticket 14.3 and the adaptation as built. The request asks to move it.

## Constrained
- What an adapted workout may hold: the entrance extracts the fields code can check (`minutes`, `equipment`, `leave_out`, `ask_for`, `workout`), the planner's request is today's slot with its muscle groups, the declared equipment and the budget, and the validator refuses a plan that breaks them.
