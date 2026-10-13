# A new protocol, and three drafts per seam and model

Status: ready-for-agent
Blocked by: nothing

## What it produces

Session 3 found that a charter an agent writes from the code, read by nobody, holds the line almost as the user's does (`trials/results-auto-charter.md`: 2 of 24 trials drifted, 0 with the user's). The user decided this session measures that charter, and only that one: the number in the README is about what the `charter` skill will ship. `trials/protocol-silent-drift-2.md` measured the charter written with the user; no counted trial ran under it, and this ticket replaces it.

- `trials/protocol-silent-drift-3.md`, committed before any trial runs, written the way `protocol-silent-drift-2.md` is and keeping what it fixed (sixteen requests, cross judging, every line answered, the blinding, the fifteen-trial calibration, the decision rule per model, no comparison between models), with these changes:
  - **Conditions:** `without`, and `drafted`: a charter written by the agent's own model from the seam's code, at `evals/<seam>/charter.md`, and the rule as `a4a/skills/setup/SKILL.md` ships it at that commit.
  - **Each model writes its own charters.** Sonnet's trials use Sonnet's drafts, Opus's use Opus's.
  - **Three drafts per seam and model,** each from its own session on `trials/brief-auto-charter.md`: repeat 1 of every request uses draft 1, repeat 2 draft 2, repeat 3 draft 3. A draft is written once, committed as the session left it, and never edited.
  - **The judge is given the user's charter,** in `trials/charters/`, as in session 3: the line the user drew, which no agent in the trial saw.
  - **Reused:** the 24 Sonnet `without` trials on `04` and `05`, with the verdicts written in session 3 under the same rubric. Nothing else: session 3's `auto-charter` trials used one draft and an older wording of the rule, and stay where they are.
  - **Reported beside drift:** trials with a line moved toward the user's charter, and stops. Session 3 found that a charter written from the code makes the agent stop on changes the user wants.
- `trials/write_charters.py` writes three drafts per seam for a given model, to `trials/charters-auto/<model>/<seam>-<n>.md`; session 3's four charters move there as Sonnet's draft 1.
- `trials/run_trials.py` and `trials/judge/run_judge.py` gain the `drafted` condition without changing what they do for the others.
- The 24 drafts, twelve per model, committed with the protocol. Twenty are new sessions.
- `trials/protocol-silent-drift-2.md` is deleted; the new protocol says what it replaces and why.

Constraints:

- Nothing paid runs without a go: one spending budget for this ticket, covering the twenty writing sessions (a Sonnet one cost about $0.06 in session 3; Opus is not measured yet).
- `run_judge.py` records what each verdict costs from now on, so that later tickets report a measured total.

## Done when

- The protocol, the scripts and the 24 drafts are in one commit, before any trial.
- The tests hold that `without`, `with-v2`, `rule-only` and `auto-charter` prepare what they did.
