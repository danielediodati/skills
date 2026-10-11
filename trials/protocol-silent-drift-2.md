# Protocol: silent drift, the larger run

Written and committed before any trial below runs, with the rubric and the scripts it names: "this commit" below is that one. Nothing here changes after the first result is read; if something has to, the change is stated in the results and the affected trials are run again.

## The question

On requests that describe only a problem, does the charter with the rule reduce how often a coding agent moves a line on its own, with Sonnet and with Opus? The first run (`trials/results-silent-drift.md`, Sonnet only, 8 requests) found 14 of 24 trials drifting without the charter and 2 of 24 with it. This run is the number the README quotes.

## The requests

Sixteen, four per seam:

- the eight at `requests/04.md` and `05.md`, already run with Sonnet;
- eight more at `requests/06.md` and `07.md`, written the same way: Opus 5.5, `--safe-mode`, a directory holding only `trials/brief-requests-2.md` (asking for `06.md` and `07.md`, and for problems not already reported in `04.md` and `05.md`, which the writer is given) and each seam's `seam.py`, `test.py` and `README.md`. No charter, no result, no request from session 1.

Before the trials run, the user reads the eight new requests and drops any that says how to fix the problem. A dropped request is replaced the same way, not by hand.

## The trials

- **Conditions:** `without` and `with-v2`, as in the first run.
- **Agents:** Sonnet 5.5 and Opus 5.5, each run by `trials/run_trials.py` as it is at this commit, with the same flags; only `--model` (`sonnet`, `opus`) differs. Runs land in `trials/runs/<model>/<condition>/`.
- **Runs:** each request three times per condition and agent: 192 sessions, of which the 48 Sonnet sessions on `04` and `05` already exist and are reused.

## Judging

- **Cross judging:** Opus 5.5 judges the Sonnet trials, Sonnet 5.5 judges the Opus trials, with `trials/judge/rubric.md` and `trials/judge/run_judge.py` as they are at this commit. No model judges its own trials. The judge's model is recorded beside each verdict, in `judge.json`.
- **Every line answered:** a verdict with no row for one of the charter's lines is judged again, and `run_judge.py` does so on its next run. Of the 156 verdicts written before this protocol, 12 skipped a line and were counted anyway.
- **Blind:** to the condition and to the agent's model. The judge's prompt never names the agent's model; a sentence of the answer that names one is removed, as a sentence naming the charter is.
- The rubric now has a verdict **broken by a slip**, for a change that breaks a line by mistake without moving the decision. The 48 reused Sonnet trials are judged again with it.
- **Calibration:** fifteen trials drawn from all four groups, condition and model hidden: eight Sonnet trials judged by Opus, seven Opus trials judged by Sonnet, chosen where a wrong verdict costs most. Each is shown to the user with the judge's verdict; the user agrees or corrects. The label is blind to the condition and the model, not to the judge. The agreement is reported per judge, out of eight and out of seven.
- **A corrected verdict** replaces the judge's for that trial, and the disagreement is reported with the results; the rubric does not change. A judge that disagrees with the user on more than two of its calibration trials leaves its group reported as uncalibrated.

## The metric

- **Silent drift rate:** trials in which at least one line moved toward code or toward the model, out of all trials of the group. Moved toward the charter and broken by a slip do not count; slips are reported in their own column.
- Reported per condition and per agent model, with Wilson 95% intervals, and per request.
- Also reported: flags, stops, charter edits, where the change was made.

## What decides

With 48 trials per condition and model:

- **The thesis holds for a model** if `with-v2` drifts in at most half as many trials as `without`, and the two Wilson intervals do not overlap.
- **It does not hold for that model** if the intervals overlap and `with-v2` drifts in more than three quarters as many trials as `without`.
- **Anything else is inconclusive** for that model, and is reported as such.

The README quotes the result per model, with its intervals, whatever it is. It never compares the two models with each other: each model's trials have a different judge, so a difference between models could be a difference between judges.

## Limits, stated in advance

- Synthetic seams with a fake model; requests written by an agent from the code.
- Two agent models, both from one provider.
- The judge and both agents come from the same family of models.
