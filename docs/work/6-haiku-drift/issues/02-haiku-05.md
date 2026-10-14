# Haiku on requests 05

Status: ready-for-agent
Blocked by: nothing

## What it produces

24 trials under `trials/runs/haiku/`: the four requests `05.md`, one per seam, three times in each condition (`without`, `drafted`), Haiku 5.5 as coding agent, under `trials/protocol-silent-drift-3.md` with the scripts and flags of its commit. Each trial judged by Sonnet 5.5.

- Both conditions run in the same session, so neither meets a different day of the models.
- The sessions spend the user's usage: agree the spending budget, say that 24 are about to run and wait for a go.
- Ticket 01 measured what a ticket weighs: $0.18 for the 24 trials and $1.21 for the 24 verdicts at API prices. The user let it run 6, then 18 at once.
- A failed session is run again by the script; one that fails twice is reported, not dropped.

## Done when

- 24 trials have a diff, an answer, `session.json` and a verdict, committed.
- No count is read yet: the results are read only in ticket 06.
