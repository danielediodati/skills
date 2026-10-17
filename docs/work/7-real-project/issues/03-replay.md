# Replay the episodes

Status: ready-for-agent

## What it produces

The replay of the cases the user chose, E1, E2, E7, E5, E6, D3 and D4, under `trials/protocol-reps-replay.md`, judged, and its result read by the protocol's rule. The protocol is frozen: a change is stated in the results and the runs it touches are made again.

The runs per session of work and the spending budget are settled with the user before the first paid call: every run is Opus. Nothing paid runs before the budget is agreed. One trial run took a quarter of an hour of Opus reading REPS without writing a file. Before E5's first run, one `claude -p --model claude-opus-5` call by hand checks that Opus 5 still answers: it did, on 2026-10-16.

## The budget agreed

The runs are paid from the user's Pro plan, whose limit is a five-hour window. D4's first run in both conditions measured one of each step, at about 5% of a window per dollar of the session's reported cost: a run without a charter 6.64 $, a run with one 2.26 $, a draft 0.59 $, a verdict about 0.55 $. The whole session comes to 185-320 $, nine to sixteen windows.

- One Opus run at a time, never in parallel: a run the limit cuts short is spent and made again.
- At most two Opus runs per window, with their verdicts.
- The `without` runs of the episodes first, each judged, since they decide which episodes go on.

## Done when

- Every chosen episode and declared move has its runs with and without a charter, or is reported as not reproduced, and the result is read by the protocol's rule.
