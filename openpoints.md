# Open points

What is still undecided or undone after the design session of 2026-10-06. Decisions already taken are in `CONTEXT.md`. Delete a point when it closes.

## Decisions

The decisions taken are in `CONTEXT.md`, numbered 1 to 14.

## The test that gated everything else

Session 1 (`trials/results.md`) showed the charter and the rule change what a coding agent does, so the remaining skills are worth writing. What it asked of `edd` is planned in session 2; the `charter` skill could also name the drift agents do not see as a move (input cleaned by code before the model reads it, a parsing rule that also catches a free field, a missing field defaulted instead of refused).

Still to check outside that session: load the plugin in a session (`claude --plugin-dir <repo>/a4a`) and see the skills appear. Only the manifests have been validated so far.

Running the trials on this machine: `trials/run_trials.py` and `trials/judge/run_judge.py` launch `claude -p` and ran without a refusal in tickets 05 and 06; deleting a tracked file was refused once, `git rm` went through. `python` is the Microsoft Store stub; tests run with `uv run --no-project python -m unittest`.

After session 1, the held-out check: a real project with seams in cascade, replaying a commit that drifted.

## Writing, after the test

- **`eval`**: to write. Cases, graders, judge calibration, the core and extended sets, the dev and held-out splits. Finished only when the cases cover every line of the charter and each grader has been seen to fail an output.
- **`setup`**: does not yet copy the eval scripts or create `evals/`.
- **The root `README.md`** is two lines.

## The `charter` skill, first use (ticket 3)

- **Path.** The skill writes `evals/<seam>/charter.md`; the trial wants `trials/charters/<seam>.md`. Let the caller choose, or say the path is the default.
- **Target and eval direction are mandatory** in the steps and the format. Written outside an eval (as in the trial) they are empty: make them optional.
- **Explain the seam first.** Input and output in one line each was not enough for the user to answer: they needed the flow in plain words, with an example input and output, before any decision.
- **Ask whether the seam needs a model at all.** On `draft_reminder` the user's first answer was that a template would do. The skill has no step for that; it assumes the model belongs there.
- **"The line moves only when the user decides it" names no one at run time.** Once the charter is written, only code, model and coding agent are left. The skill should say the charter is where the decision lives, and that an agent who cannot meet a request without moving a line stops and says so (the `setup` rule above).
- **A line the code does not yet hold.** The user put two decisions on the constrained side that the code does not apply (ISO currency list, VAT as a separate field). The format has no place for that; `extract_invoice` marks them "Not yet in code".

## `edd`, first real run (the demo of session 2)

Found by the demo on `triage_ticket`; the run and the evidence are in `trials/results-edd-demo.md`.

- **Dollars with two decimals.** A run under a cent prints and logs as `$0.00`, and so does its estimate.
- **Tagging failures discards the best results.** The loop asks for the failure category in the case's `tags`; a change to the eval set discards every best result.
- **The runner keeps outcomes, not outputs.** Reading a failure means paying for the call again, unless the adapter saves the answers itself.
- **A first run below the target becomes the model's best result.**
- **`--model` only changes the label.** The runner logs it and never hands it to the adapter, which has to read the model from the environment.
- **`triage_ticket`: the enterprise raise.** A routine enterprise request the model calls `high` comes out `urgent` (`tt-12`, `requests/07`). Changing the raise moves a constrained line: the user's decision, not taken.
- **`triage_ticket`: a grader that wants words.** `summary_any` failed a right summary once (`tt-11`); a model judge would need calibrating first.

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
