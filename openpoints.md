# Open points

What is still undecided or undone. Decisions already taken are in `CONTEXT.md`; work that has a ticket is in `ROADMAP.md`. Delete a point when it closes.

## Machine and plugin

- Still to check: load the plugin in a session (`claude --plugin-dir <repo>/a4a`) and see the skills appear. Only the manifests have been validated so far. Ticket 3.6.
- Running the trials on this machine: `trials/run_trials.py` and `trials/judge/run_judge.py` launch `claude -p` without a refusal; deleting a tracked file was refused once, `git rm` went through. `python` is the Microsoft Store stub; tests run with `uv run --no-project python -m unittest`. A `bash` heredoc that holds Python with apostrophes has failed to parse more than once: write the script to a file.

## The charter, after session 3

Five arms on the same 24 trials (`trials/results-rule-only.md`, `results-auto-charter.md`, `results-practice-charter.md`): drift in 15 with nothing, 11 with the rule alone, 2 with a charter the agent wrote from the code as it is, 2 with one it wrote by its own rules, 0 with the user's. A line moved toward what the user wants in 8, 9, 6, 5 and 12.

Decided by the user, to be written into the skills by ticket 3.4:

- **The agent writes the charter alone.** It asks only on a serious doubt, otherwise nothing; with nobody to answer, it chooses and marks the line.
- **The charter states the line as the code has it.** The user validated that brief (`trials/brief-auto-charter.md`) after trying the other: the agent reasoning by its own rules did no better and stopped more. The `charter` skill and session 4 use it as it is.
- **A charter holds free, constrained and budget.** Target and eval direction move to the `eval` skill.
- **`CONTEXT.md` decision 7 stands;** it could say who writes the charter. The rule `setup` writes loses "with the user" from "write one with the user first".

Still open:

- **The stiffness is not solved.** Either charter makes the agent stop on changes the user wants (10 and 13 stops in 24), because nobody told it which of today's behaviours are defects. Only the user's charter did, and no brief found a way around a person knowing what the seam is for.
- **A charter that judges the code can be wrong the other way:** two of nine lines the agent marked as defects are things the user wants.
- **A drift agents do not see as a move** could be named by the skill or the rule: input cleaned by code before the model reads it, a parsing rule that also catches a free field, a missing field defaulted instead of refused. From session 1; no ticket.
- Not measured: a real seam spread over a project (session 7); how much several drafts of one seam differ (session 4); a draft reviewed by the user against a charter written with the user (no ticket).

## Writing, after the test

- **`eval`**: to write. Cases, graders, judge calibration, the core and extended sets, the dev and held-out splits. Finished only when the cases cover every line of the charter and each grader has been seen to fail an output.
- **`setup`**: does not yet copy the eval scripts or create `evals/`.
- **The root `README.md`** is two lines. Sessions 5 and 6 give it its numbers; teaching the vocabulary through one example has no ticket.

## Known weak spots

Ticket 3.6 moves the standing limits among these to `CONTEXT.md`.

- **Over-delegation** has no real episode behind it yet. **Substitution** and **templating** were derived from one project's documents and confirmed in passing.
- **Spotting drift in a diff is the hardest check.** Telling a legitimate constraint (a closed list of valid ids) from templating (a closed list of styles) takes judgement; false alarms would get it ignored.
- **Process weight.** Charter, eval set and loop for every seam is a lot for a small project. The charter is cheap and the eval set is not: say what can be done without the rest. The charter itself cannot be skipped, and the agent can write it alone (session 3 above).
- **A charter can go stale.** If the line moves on purpose and the charter is not updated in the same change, the charter becomes the wrong thing.
- **Vocabulary load.** Seam, stochastic seam, charter, drift, substitution, templating, over-delegation, target, noise floor. The README has to teach them through one example, start to finish.
- **`CONTEXT.md` decision 2** still allows "wrappers or optional references" to external skills, against the no-cross-references rule. Rewrite or drop it.

## Repo

Ticket 3.6.

- **One ADR is worth writing**: the central rule (freedom and constraint, symmetric) replacing the earlier one-way rule. It is the choice a later reader would find least obvious.

## Parked

Ticket 3.6 moves these to the end of `ROADMAP.md`.

- Hosts other than Claude Code (version 2).
- Candidate skills: `budget`, `agent-topology`, `failure-triage`, `context-budget`.
- The author's personal `roadmap` skill, outside this repo: support for GitHub Issues, sessions against milestones.
