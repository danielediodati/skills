# Open points

What is still undecided or undone after the design session of 2026-10-06. Decisions already taken are in `CONTEXT.md`. Delete a point when it closes.

## Decisions

None open. The decisions taken are in `CONTEXT.md`, numbered 1 to 13.

## The test that gates everything else

The plugin rests on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does. Test it before writing the remaining skills.

1. Load the plugin in a session on a real project (`claude --plugin-dir <repo>/a4a`) and check the skills appear. Only the manifests have been validated so far.
2. Run `setup`, then `charter` on one seam.
3. Give a coding agent the same task twice, on two branches: once with the charter and the rule, once without. Pick tasks that produced drift before.
4. Compare the diffs: did the free decisions stay with the model? Two or three tasks; one proves nothing.

## Writing, after the test

- **`edd`**: remove the references to external skills, replace the one-way rule ("a model seam becomes code only when an eval shows...") with the symmetric one, rename "model seam" to "stochastic seam", move cases and graders out to `eval`, replace smoke and full runs with the core and extended sets, replace the baseline with best results per model (fail below the target, warn below the best result), check the diff against the charter before accepting a change, and say it runs only when a stochastic seam changes. The scripts change with it.
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
