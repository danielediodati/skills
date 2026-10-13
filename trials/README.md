# Trials

The scripts that run the charter trials and judge them, with their briefs, protocols and results.

## Running them on this machine

- `run_trials.py`, `write_charters.py` and `judge/run_judge.py` launch `claude -p`, and run without a refusal.
- `python` is the Microsoft Store stub. Tests and scripts run with `uv run --no-project python`, e.g. `uv run --no-project python -m unittest discover -s tests`.
- Deleting a tracked file was refused once; `git rm` went through.
- A `bash` heredoc that holds Python with apostrophes or backslashes has failed to parse more than once: write the script to a file and run the file.
