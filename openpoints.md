# Open points

What is still undecided or undone after the design session of 2026-10-06. Decisions already taken are in `CONTEXT.md`. Delete a point when it closes.

## Decisions

The decisions taken are in `CONTEXT.md`, numbered 1 to 13. One is open:

- **What session 1's gate can conclude.** The trial's seams run a fake model, so the coding agent sees one failure reported in a request and never a model that keeps failing after a prompt fix. In the project the drift terms came from, code closing in on a small model after repeated failures is on record (formats and legality, mostly), next to drift designed in before any model ran. Fewer than 12 drifted trials of 36 would say drift is rare on the first move, not that it is residual. To decide before ticket 05 runs: keep the stop rule, or below the gate repeat on one seam with a real small model and an eval the agent can run.

## The test that gates everything else

The plugin rests on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does. It is tested before the remaining skills are written: session 1 in `ROADMAP.md`, six tickets under `docs/work/1-charter-trial/issues/`.

Still to check outside that session: load the plugin in a session (`claude --plugin-dir <repo>/a4a`) and see the skills appear. Only the manifests have been validated so far.

After session 1, the held-out check: a real project with seams in cascade, replaying a commit that drifted.

## Writing, after the test

- **`edd`**: remove the references to external skills, replace the one-way rule ("a model seam becomes code only when an eval shows...") with the symmetric one, rename "model seam" to "stochastic seam", move cases and graders out to `eval`, replace smoke and full runs with the core and extended sets, replace the baseline with best results per model (fail below the target, warn below the best result), check the diff against the charter before accepting a change, and say it runs only when a stochastic seam changes. The scripts change with it.
- **`edd`, the way out of a seam its model cannot hold**: when the runs stay below the target with the charter intact and the seam's budget is spent, `edd` stops and says so. It is the budget that ends the loop: on code the coding agent regulates itself, but every eval run costs. `edd` then puts the ways out to the user and takes none itself: another model (best results are kept per model, so the report shows whether one clears the target), the line moved on purpose (a charter change, the eval run on both versions, an ADR), a lower target, or the failure accepted. A model change is recommended with its evidence: what was tried on the model's side and how it failed.
- **`setup`, one more line in the `AGENTS.md` rule**: if the request cannot be met without moving a line of the charter, stop and say so.
- **`eval`**: to write. Cases, graders, judge calibration, the core and extended sets, the dev and held-out splits. Finished only when the cases cover every line of the charter and each grader has been seen to fail an output.
- **`setup`**: does not yet copy the eval scripts or create `evals/`.
- **`a4a/README.md`**: still describes the old `edd`; lines about wiring and install mention the former `dd` plugin. The root `README.md` is two lines.

## Known weak spots

- **Over-delegation** has no real episode behind it yet. **Substitution** and **templating** were derived from one project's documents and confirmed in passing.
- **Spotting drift in a diff is the hardest check.** Telling a legitimate constraint (a closed list of valid ids) from templating (a closed list of styles) takes judgement; false alarms would get it ignored.
- **Process weight.** Charter, eval set and loop for every seam is a lot for a small project. The charter is cheap and the eval set is not: say what can be done without the rest.
- **A charter can go stale.** If the line moves on purpose and the charter is not updated in the same change, the charter becomes the wrong thing.
- **Vocabulary load.** Seam, stochastic seam, charter, drift, substitution, templating, over-delegation, target, noise floor. The README has to teach them through one example, start to finish.
- **`CONTEXT.md` decision 2** still allows "wrappers or optional references" to external skills, against the no-cross-references rule. Rewrite or drop it.

## Repo

- **One ADR is worth writing**: the central rule (freedom and constraint, symmetric) replacing the earlier one-way rule. It is the choice a later reader would find least obvious.
- **`.vscode/`** is untracked on purpose: personal editor settings.

## Parked

- Hosts other than Claude Code (version 2).
- Candidate skills: `budget`, `agent-topology`, `failure-triage`, `context-budget`.
- The author's personal `roadmap` skill, outside this repo: support for GitHub Issues, sessions against milestones.
