# Freeze the protocol and ready the scripts

Status: ready-for-agent
Blocked by: nothing

## What it produces

- `trials/protocol-silent-drift-2.md` final, with "Draft" removed and the cross judging written in: Opus judges the Sonnet trials, Sonnet judges the Opus trials, and the README never compares the two models with each other. Seven of the fifteen calibration trials come from Opus trials judged by Sonnet.
- `trials/judge/rubric.md` with the **broken by a slip** verdict (already in the working tree): read once more against the two `action_items 04` trials that motivated it.
- `trials/run_trials.py`: a `--model` option (`sonnet`, `opus`) and a `--requests` filter (`04 05`, `06`...). Runs land in `trials/runs/<model>/<condition>/<trial>/`; the existing Sonnet runs move under `trials/runs/sonnet/` with `git mv`, and every script and results file that reads them follows.
- `trials/judge/run_judge.py`: the judge is the model that did not run the trial, chosen from the run's `session.json`; the judge's model is recorded beside each verdict. The judge's prompt never names the agent's model.
- A dry check: one trial of each model on one request, judged, without counting toward any result.

## Done when

- The protocol, the rubric and the scripts are committed together, before any counted trial runs: that commit is the one the protocol names.
- The dry check produced a diff, an answer and a verdict for each model, and the dry runs are deleted.
