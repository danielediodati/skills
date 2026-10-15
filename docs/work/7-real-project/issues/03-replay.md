# Replay the episodes

Status: needs-triage
Blocked by: 7.2

## What it produces

The replay of the cases the user chose, E1, E2, E7, E5, E6, D3 and D4, under `trials/protocol-reps-replay.md`, judged, and its result read by the protocol's rule. The protocol is frozen: a change is stated in the results and the runs it touches are made again.

The runs per session of work and the spending budget are settled with the user before the first paid call: every run is Opus. Nothing paid runs before the budget is agreed. Before E5's first run, one `claude -p --model claude-opus-5` call by hand checks that Opus 5 still answers.

## Done when

- Every chosen episode and declared move has its runs with and without a charter, or is reported as not reproduced, and the result is read by the protocol's rule.
