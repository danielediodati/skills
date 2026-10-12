# Formats

## `evals/<seam>/cases.jsonl`

The eval set: one JSON object per line. A run names it in the environment, `EVAL_SET=cases.jsonl`, never by a path in the code; the runner refuses to start without it and logs it on every row.

```json
{"id": "planner-017", "split": "dev", "core": true, "input": {"request": "45 minutes, no barbell, sore left knee"}, "expected": null, "rubric": ["Every exercise avoids loaded knee flexion", "Total duration is between 40 and 50 minutes"], "source": "trace 2026-09-30, user complaint", "tags": ["injury-constraint", "equipment"]}
```

- `id`: stable and never reused, so log rows and accepted losses stay traceable.
- `split`: `dev` or `heldout`.
- `core`: `true` puts the case in the core set, the few cases (5 to 10 per split) that run first on every change. A split with no core case refuses to run. Core and extended are a different axis from dev and held-out: each split has its own core set.
- `expected` and `rubric`: at least one of the two is set. `expected` feeds a structural, execution or reference grader; `rubric` feeds a model judge.
- `source`: where the case came from (a trace, a ticket, the spec, grilling). Cases born from real failures are the most valuable; keep the link back to them.
- `tags`: failure categories and slices, so a run reports per-tag scores next to the total.

## `evals/<seam>/system.py` and `evals/<seam>/grader.py`

The contract `run_evals.py` expects:

```python
# system.py: runs one case through the system under test.
MODEL = "llama-3.3-70b-versatile"  # logged on every row; --model overrides
PROVIDER = "groq"                  # logged on every row; --provider overrides
COST_PER_CASE = 0.0006             # dollars per call, the estimate before a run; 0 for a free local model

def run(case_input: dict) -> dict:
    # Call the real entry point (graph, agent, endpoint) with case_input.
    # Return {"output": ...} plus, when known, "tokens" (int), "seconds" (float)
    # and "cost" (float, dollars this call cost; COST_PER_CASE is used when it is missing).
    ...

# grader.py: one grader per seam, versioned with the cases.
def grade(case: dict, result: dict) -> bool | float:
    # True or False, or a score in [0, 1] that passes at 0.5 or above.
    ...
```

A grader at rung 4 calls the judge:

```python
from judge import judge

def grade(case, result):
    verdicts = judge(rubric=case["rubric"], output=result["output"], context=case["input"])
    return all(v["pass"] for v in verdicts)
```

## `evals/<seam>/calibration.jsonl`

One output you labelled yourself per line, `human` aligned with `rubric`:

```json
{"id": "cal-07", "input": {"request": "30 minutes, hotel room"}, "output": "...", "rubric": ["Uses no equipment", "Fits in 30 minutes"], "human": [true, false]}
```

## `evals/<seam>/runs/<run-id>.json`

Written by the runner, never edited: the run's settings (eval set, split, `k`, model, provider, commit), the hashes of the eval set and `grader.py`, whether the run is the `core` set or the `extended` set, the per-run scores, and for every case its `k` outcomes, its majority result, its cost and any errors. A run whose core set passes writes two files: the core run, then the extended run, which reuses the core results instead of paying for them again.

## `evals/<seam>/best.json`

Written by the runner, never edited: for each split, the best result of each model on the extended set, with its per-run scores, the run it came from and the code version it was measured on. It also holds the eval set and the hashes of the eval set and `grader.py` the results were measured with: when either hash changes, the runner discards every best result (the measure changed) and says so. A change to the code keeps them, reported as measured on an earlier version.

## `evals/spending.json`

Written by the runner: the spending budget the user agreed for the current ticket (`--agree-budget <dollars> --note "<ticket>"`), what has been spent against it, and the cost of each run. A new budget with the same `--note` raises the budget and keeps the total; a budget for another ticket starts the total at zero. The runner refuses to start a run whose estimate, core and extended sets together, would take the total past the budget, and checks again before the extended set; a run whose estimate is zero (a free local model) needs no budget. The estimate prices a call at the mean cost per call of this model's latest run, else at `COST_PER_CASE`.

## `evals/log.md`

One row per run, newest last, appended by the runner:

| date | commit | seam | eval set | model | provider | split | set | k | score | spread | gains/losses | cost/case | cost | spent | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-02 | a1b2c3d | planner | cases.jsonl | llama-3.3-70b-versatile | groq | dev | core | 3 | 0.83 | 0.80 to 0.90 | - | 2.0k tok, 1.3 s | $0.02 | $0.02 | - |
| 2026-10-02 | a1b2c3d | planner | cases.jsonl | llama-3.3-70b-versatile | groq | dev | extended | 3 | 0.71 | 0.67 to 0.75 | - | 2.1k tok, 1.4 s | $0.05 | $0.07 | - |
| 2026-10-03 | e4f5a6b+dirty | planner | cases.jsonl | llama-3.3-70b-versatile | groq | dev | core | 3 | 0.60 | 0.50 to 0.70 | - | 2.3k tok, 1.5 s | $0.02 | $0.09 | tool descriptions rewritten |

- `eval set`: the file named by `EVAL_SET`.
- `set`: `core` or `extended`; `calibration` for a judge calibration. A `core` row with no `extended` row after it is a change rejected on the core set.
- `score` and `spread`: defined in SKILL.md, Noise floor.
- `gains/losses`: paired against the run that holds this model's best result, with the one-sided sign-test p-value.
- `cost/case`: mean tokens and seconds per case run. `cost`: the dollars this row paid for; an extended row pays only for the cases beyond the core set, whose results it reuses. `spent`: the running total against the agreed budget after this row, `-` when no budget is agreed.
- `notes`: the one change under test from `--note`, the losses listed by id (keeping the change accepts them), and `best results discarded` when the grader or the eval set changed.
