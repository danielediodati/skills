# Formats

## `evals/<seam>/cases.jsonl`

The eval set: one JSON object per line. A run names it in the environment, `EVAL_SET=cases.jsonl`, never by a path in the code; the runner refuses to start without it and logs it on every row. A seam may keep more than one eval set (a set being drafted, a redefined one); each is a file in the seam's directory.

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
MODEL = "qwen3.5:9b"   # logged on every row; --model overrides
PROVIDER = "ollama"    # logged on every row; --provider overrides

def run(case_input: dict) -> dict:
    # Call the real entry point (graph, agent, endpoint) with case_input.
    # Return {"output": ...} plus, when known, "tokens" (int) and "seconds" (float).
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

Written by the runner, never edited: the run's settings (eval set, split, `k`, model, provider, commit), the hashes of the eval set and `grader.py`, whether the run is the `core` set or the `extended` set, the per-run scores, and for every case its `k` outcomes, its majority result, its cost and any errors. A run whose core set passes writes two files: the core run, then the extended run, which reuses the core results instead of paying for them again. `runs/baseline-<split>.txt` holds the id of the current baseline run for each split.

## `evals/log.md`

One row per run, newest last, appended by the runner:

| date | commit | seam | eval set | model | provider | split | set | k | score | spread | gains/losses | cost/case | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-02 | a1b2c3d | planner | cases.jsonl | qwen3.5:9b | ollama | dev | core | 3 | 0.83 | 0.80 to 0.90 | - | 2.0k tok, 13.1 s | - |
| 2026-10-02 | a1b2c3d | planner | cases.jsonl | qwen3.5:9b | ollama | dev | extended | 3 | 0.71 | 0.67 to 0.75 | - | 2.1k tok, 14.0 s | first baseline; promoted |
| 2026-10-03 | e4f5a6b+dirty | planner | cases.jsonl | qwen3.5:9b | ollama | dev | core | 3 | 0.60 | 0.50 to 0.70 | - | 2.3k tok, 15.2 s | tool descriptions rewritten |

- `eval set`: the file named by `EVAL_SET`.
- `set`: `core` or `extended` for a run; `promote` when `--promote-last` makes the latest extended run the baseline; `calibration` for a judge calibration. A `core` row with no `extended` row after it is a change rejected on the core set.
- `score` and `spread`: defined in SKILL.md, Noise floor.
- `gains/losses`: paired against the baseline run, with the one-sided sign-test p-value.
- `notes`: the one change under test from `--note`, the losses listed by id (promoting the run accepts them), `promoted` when a run became the baseline as it ran, and `provisional` (pass it as `--note` with `--promote-last`) when you keep a gain with p above 0.05.
