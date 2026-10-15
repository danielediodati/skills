# Runs

The raw trials, as `run_trials.py` wrote them: `<model>/<condition>/<seam>-<request>-<repeat>/`, with the agent's diff, its final answer, the session's numbers and the verdicts.

A run is not edited after it is written, with one exception: the two answers that quoted a local path (`haiku/without/recommend_products-06-3`, `sonnet/without/triage_ticket-01-2`) have the trials' temporary directory replaced by `<work>`. Nothing else in any run has changed.
