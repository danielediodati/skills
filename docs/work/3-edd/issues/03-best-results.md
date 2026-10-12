# Best results per model replace the baseline

Status: ready-for-agent
Blocked by: 02

## What it produces

`edd` and `run_evals.py` judge a run as decisions 12 and 13 say:

- Below the charter's target: failure, the only one.
- At or above the target but below that model's best result by more than the run-to-run spread: a warning in the report.
- Best results are kept per model, each with the code version it was measured on. A change to the grader or the eval set discards a seam's best results; a change to the seam's code keeps them, marked as measured on an earlier version.
- The words "baseline" and `--promote-last` go.

## Done when

- Unit tests show each case: below target fails; below best result within the spread passes with no warning; beyond the spread passes with a warning; a grader change empties the best results; a code change marks them out of date.
