# The tree cleaned

Status: ready-for-agent
Blocked by: 01

## What it produces

A tree with nothing of the author's machine in it, on `main` and on `session-7-reps`.

- The scripts and tests that name a local directory read it from an environment variable, with a default relative to the repo or the system's temporary directory. A test that needs REPS is skipped where REPS is not.
- The two raw runs that quote a local path (`recommend_products-06-3`, `triage_ticket-01-2`) have it replaced by `<work>`, and the runs' README says so: the only change ever made to a run after it was written.
- `tests/test_run_evals.py` checks what it checks without committing to a repository, so it sets no git option of its own.
- The ignored caches deleted.

## Done when

- No tracked file names the author's home directory.
- The full test suite is green on both branches.
