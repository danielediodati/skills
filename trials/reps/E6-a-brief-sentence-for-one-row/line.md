# E6 - the line a replay is judged on

Seams: planner (`src/trainer/coach/planner.py`, `src/trainer/plan.py`)

Where the design puts it: `1057b2a`, the planner reads the user's words about today, and ADR-0010 item 4, where a reading of the user's words is held at a judgement bar, not by code.

## Free
- How the planner reads a movement the user leaves out today, as in «oggi niente squat, proponi tu»: it reads the sentence and decides what is out. A rule written for one eval row, in the brief or in code, that settles how a named movement is read (every variant out, a pattern removed, a list of names) takes that reading from the model. Moving a miss of reading to a judgement bar, or measuring the reading again, does not.
