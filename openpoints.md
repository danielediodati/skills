# Open points

What is still undecided or undone after the design session of 2026-10-06. Decisions already taken are in `CONTEXT.md`. Delete a point when it closes.

## Decisions

The decisions taken are in `CONTEXT.md`, numbered 1 to 13.

## The test that gated everything else

The plugin rested on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does. Session 1 tested it (`trials/results.md`): without the charter 27 of 36 trials drifted and no agent said so; with the charter and the rule as it ships now, 12 drifted, and agents flagged the line 17 times and stopped 11 times. The claim holds, so **the remaining skills are worth writing**, with three consequences:

- **The first rule had a back door**: 21 of 36 agents rewrote the charter to fit their change. The rule now says only the user changes a charter, and no agent edited it.
- **`edd` must check the diff against the charter as it was before the change**, never the one in the working tree: an agent that moved a line can rewrite the charter in the same diff.
- **The drift left is the kind the agent does not see as a move**: input cleaned by code before the model reads it, a parsing rule that also catches a free field, a missing field defaulted instead of refused. That is the diff check's job in `edd`, and the examples the rule or the `charter` skill could name.

Still to check outside that session: load the plugin in a session (`claude --plugin-dir <repo>/a4a`) and see the skills appear. Only the manifests have been validated so far.

Running the trials on this machine: `trials/run_trials.py` and `trials/judge/run_judge.py` launch `claude -p` and ran without a refusal in tickets 05 and 06; deleting a tracked file was refused once, `git rm` went through. `python` is the Microsoft Store stub; tests run with `uv run --no-project python -m unittest`.

After session 1, the held-out check: a real project with seams in cascade, replaying a commit that drifted.

## Writing, after the test

- **`edd`**: remove the references to external skills, replace the one-way rule ("a model seam becomes code only when an eval shows...") with the symmetric one, rename "model seam" to "stochastic seam", move cases and graders out to `eval`, replace smoke and full runs with the core and extended sets, replace the baseline with best results per model (fail below the target, warn below the best result), check the diff against the charter before accepting a change, and say it runs only when a stochastic seam changes. The scripts change with it.
- **`edd`, the way out of a seam its model cannot hold**: when the runs stay below the target with the charter intact and the seam's budget is spent, `edd` stops and says so. It is the budget that ends the loop: on code the coding agent regulates itself, but every eval run costs. `edd` then puts the ways out to the user and takes none itself: another model (best results are kept per model, so the report shows whether one clears the target), the line moved on purpose (a charter change, the eval run on both versions, an ADR), a lower target, or the failure accepted. A model change is recommended with its evidence: what was tried on the model's side and how it failed.
- **`setup`, one more line in the `AGENTS.md` rule**: if the request cannot be met without moving a line of the charter, stop and say so.
- **`eval`**: to write. Cases, graders, judge calibration, the core and extended sets, the dev and held-out splits. Finished only when the cases cover every line of the charter and each grader has been seen to fail an output.
- **`setup`**: does not yet copy the eval scripts or create `evals/`.
- **`a4a/README.md`**: still describes the old `edd`; lines about wiring and install mention the former `dd` plugin. The root `README.md` is two lines.

## The `charter` skill, first use (ticket 3)

- **Path.** The skill writes `evals/<seam>/charter.md`; the trial wants `trials/charters/<seam>.md`. Let the caller choose, or say the path is the default.
- **Target and eval direction are mandatory** in the steps and the format. Written outside an eval (as in the trial) they are empty: make them optional.
- **Explain the seam first.** Input and output in one line each was not enough for the user to answer: they needed the flow in plain words, with an example input and output, before any decision.
- **Ask whether the seam needs a model at all.** On `draft_reminder` the user's first answer was that a template would do. The skill has no step for that; it assumes the model belongs there.
- **"The line moves only when the user decides it" names no one at run time.** Once the charter is written, only code, model and coding agent are left. The skill should say the charter is where the decision lives, and that an agent who cannot meet a request without moving a line stops and says so (the `setup` rule above).
- **A line the code does not yet hold.** The user put two decisions on the constrained side that the code does not apply (ISO currency list, VAT as a separate field). The format has no place for that; `extract_invoice` marks them "Not yet in code".

## Known weak spots

- **Over-delegation** has no real episode behind it yet. **Substitution** and **templating** were derived from one project's documents and confirmed in passing.
- **Spotting drift in a diff is the hardest check.** Telling a legitimate constraint (a closed list of valid ids) from templating (a closed list of styles) takes judgement; false alarms would get it ignored.
- **Process weight.** Charter, eval set and loop for every seam is a lot for a small project. The charter is cheap and the eval set is not: say what can be done without the rest.
- **A charter can go stale.** If the line moves on purpose and the charter is not updated in the same change, the charter becomes the wrong thing.
- **Vocabulary load.** Seam, stochastic seam, charter, drift, substitution, templating, over-delegation, target, noise floor. The README has to teach them through one example, start to finish.
- **`CONTEXT.md` decision 2** still allows "wrappers or optional references" to external skills, against the no-cross-references rule. Rewrite or drop it.

## Repo

- **One ADR is worth writing**: the central rule (freedom and constraint, symmetric) replacing the earlier one-way rule. It is the choice a later reader would find least obvious.

## Parked

- Hosts other than Claude Code (version 2).
- Candidate skills: `budget`, `agent-topology`, `failure-triage`, `context-budget`.
- The author's personal `roadmap` skill, outside this repo: support for GitHub Issues, sessions against milestones.
