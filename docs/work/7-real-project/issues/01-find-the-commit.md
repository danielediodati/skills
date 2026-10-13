# Find a commit that drifted, in REPS

Status: ready-for-agent
Blocked by: nothing

## What it produces

Every result so far is on four synthetic seams of one file each. The user named the real project to check against: REPS (`source/personal/REPS`), which has seams in cascade. The commit is to be found.

- A search of REPS's history for changes to a stochastic seam where a decision moved between the model and code without anyone deciding it: a constant, a default, a closed list or a fixed reply taking over what the model decided, or a check loosened.
- For each candidate: the commit, the seam, the line that moved, the request that led to it if the history shows it, and whether the state before it can be checked out and run.
- One candidate proposed to the user for the replay, with the reason, and the others listed.
- The tickets of the replay itself are written with the user once the commit is chosen: this session has no more until then.

Reading the history costs nothing.

## Done when

- The candidates are in a file in this session's directory, and the user has chosen one or said none fits.
