# Sonnet on requests 07

Status: ready-for-agent
Blocked by: nothing

## What it produces

24 trials under `trials/runs/sonnet/`: the four requests `07.md`, one per seam, three times in each condition (`without`, `drafted`), Sonnet 5.5 as coding agent, under `trials/protocol-silent-drift-3.md` with the scripts and flags of its commit. Each trial judged by Opus 5.5.

- Both conditions run in the same session, so neither meets a different day of the models.
- The sessions spend the user's usage: agree the spending budget, say that 24 are about to run and wait for a go.
- The spending budget is a share of the account's usage window, which is never exhausted: the user reads `/usage`, the agent cannot. Ticket 01 measured about 10 points of the window per dollar at API prices, and $4.10 for 24 trials and 24 verdicts; ticket 02, with both conditions, $5.05: run a batch of six, ask for the reading, then project.
- A failed session is run again by the script; one that fails twice is reported, not dropped.

## Done when

- 24 trials have a diff, an answer, `session.json` and a verdict, committed.
- No count is read yet: the results are read only in ticket 05.
