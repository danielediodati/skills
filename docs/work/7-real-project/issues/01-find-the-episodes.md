# Find the drift episodes in REPS

Status: ready-for-agent
Blocked by: nothing

## What it produces

Every result so far is on four synthetic seams of one file each. The user named the real project to check against: REPS (`source/personal/REPS`), which has seams in cascade. This ticket finds as many drift episodes in its history as it holds.

- A pass over every commit of REPS that touches the code or the prompts of a stochastic seam, in both directions: toward code (substitution, templating) and toward the model (over-delegation).
- The unit is the drift episode (`CONTEXT.md`), not the single commit. A move declared at the time is listed apart, as a contrast case.
- For each episode and each declared move: the commits, the seam, the line that moved, the model that made it (Opus 5 or Opus 5.5), the request that led to it and where it comes from (the session transcript, local from 14 September, else the ticket), and whether the parent commit can still be checked out and run.
- One episode written up per finding, plus a list, in `docs/work/7-real-project/episodes/`. That folder is kept out of git (`.git/info/exclude`): it quotes REPS's code and the user's messages, and this repo is meant to be public. Where the raw material lives for good is decided with the user once the findings are in.

Reading the history costs nothing.

## Done when

- The episodes and the declared moves are written up, the user has chosen which ones the replay runs, and where the raw material lives is decided.
