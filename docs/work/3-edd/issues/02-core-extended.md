# Core and extended sets replace smoke and full runs

Status: ready-for-agent
Blocked by: 01

## What it produces

`edd` and `run_evals.py` run a seam in the order of decision 11: the core set first, the extended set only if the core set passes. A change that fails the core set is rejected without a call spent on the rest.

- A case belongs to the core set by a field in `cases.jsonl` (`FORMAT.md` says which).
- Every run names its eval set by a fixture given in the environment (a variable the runner reads, e.g. `EVAL_SET`), never by a path inside the code, and logs it on its row. A run without it refuses to start.
- Dev and held-out stay a separate axis from core and extended.

## Done when

- Unit tests of `run_evals.py` (standard library only, `uv run --no-project python -m unittest`) show: a failing core set stops the run before the extended set; a run with no fixture in the environment exits with a message naming the variable.
