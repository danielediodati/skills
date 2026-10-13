# Five defects of the eval runner

Status: ready-for-agent
Blocked by: nothing

## What it produces

`edd` is the skill that, when a prompt changes, runs it on a set of cases and says whether the score holds. Its runner, `a4a/skills/edd/scripts/run_evals.py`, was used once for real (`trials/results-edd-demo.md`), and five things went wrong. Each is fixed test-first, in `tests/test_run_evals.py`.

1. **Small costs cannot be read.** A run of half a cent prints and logs as `$0.00`, and so does its estimate. Costs show enough decimals to be told apart.
2. **Labelling a failure throws the records away.** Writing on a failed case what kind of failure it was (its `tags`) counts as a change to the eval set, and that discards every best result. Tags describe a case and do not change it: editing them discards nothing.
3. **The model's answers are not kept.** The runner saves passed or failed; reading what the model answered means calling it, and paying, again. Every run saves its outputs.
4. **A bad first run becomes the record.** A first run at 60% against a target of 80% is saved as the model's best result. A run below the target is recorded and is not called the best result.
5. **Choosing a model does not change it.** `--model` is logged and never reaches the adapter, which goes on using the one in its environment. The runner hands it over.

`a4a/skills/edd/SKILL.md`, `FORMAT.md` and `a4a/README.md` follow where they describe what changed.

## Done when

- Each of the five has a test that failed before the fix and passes after.
- The full suite passes.
- `openpoints.md` loses the section on `edd`'s first real run.
