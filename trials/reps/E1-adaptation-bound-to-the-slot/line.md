# E1 - the line a replay is judged on

Seams: entrance (`src/trainer/coach/entrance.py`); planner (`src/trainer/coach/planner.py`, `src/trainer/plan.py`)

Where the design puts it: ADR-0008 item 6, and ticket 10.3, which names today's workout of the mesocycle as the adaptation's starting point.

## Free
- What an adapted workout trains, with what and for how long: the planner reads what the user says about today, and today's workout of the mesocycle is its starting point, not a bound. What binds every plan still binds (the catalog, the user's exclusions); binding the adaptation to the slot's muscle groups, its admissible set, its equipment or its budget, or refusing an adaptation because it names another workout of the cycle, takes the decision from the planner.
