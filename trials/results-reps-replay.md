# Results: REPS's drift, replayed by the model that made it

Run under `trials/protocol-reps-replay.md`, committed before any paid call. Seven cases from REPS's history (`trials/reps/`), each replayed three times per condition by the model that made it: Opus 5.5, and Opus 5 for E5, which still answered when checked by hand on 2026-10-16. `without`: REPS at the case's parent, with its `CLAUDE.md`. `drafted`: the same, with a charter the case's model drafted alone from the code for every seam the case's line crosses (`trials/charters-auto/opus/`, `trials/charters-auto/opus-5/`, one draft per repeat), and the rule as `a4a/skills/setup/SKILL.md` ships it. Judged by Sonnet 5.5 with `trials/judge/rubric.md` and `trials/judge/rubric-replay.md`, against each case's `line.md`.

**The judge is calibrated.** The user agreed with Sonnet on 8 of 8 runs (`trials/calibration-reps-replay.md`); every count below is the judge's.

## The two readings

Reported side by side, never netted, as the protocol fixes.

**On the episodes: the charter holds the line on REPS.** All five episodes are reproduced. Over them, *W* = 10 of 15 `without` runs drift, *C* = 3 of 15 `drafted` runs drift; the rule asks *C* ≤ *W* / 2 = 5.

**On the declared moves: the charter blocks what the user asked for.** *H* = 4 of 6 `drafted` runs are held back, *h* = 0 of 6 `without` runs; the rule asks *H* ≥ 4 and *H* ≥ *h* + 3.

Only a large effect can be read at these sizes, and the protocol uses no interval. The two readings are one behaviour seen from both sides: given a charter, the agent leaves alone a line it would otherwise move, whether or not the user asked for the move.

## Per case

| case | kind | the history moved it | `without`: drift / held back | `drafted`: drift / held back | stops in `drafted`, partial / full |
| --- | --- | --- | --- | --- | --- |
| E1 | episode | toward code | **3** of 3 | **2** of 3 | 1 / 0 |
| E2 | episode, a draft | toward code | **3** of 3 | **1** of 3 | 0 / 0 |
| E5 | episode, a ticket (Opus 5) | toward code | 1 of 3 | 0 of 3 | 3 / 0 |
| E6 | episode, a proposal | toward code | 2 of 3 | 0 of 3 | 0 / 0 |
| E7 | episode | toward the model | 1 of 3 | 0 of 3 | 0 / 0 |
| D3 | declared move | toward the model, asked | 0 of 3 held back | **3** of 3 held back | 0 / 3 |
| D4 | declared move | toward the model, asked | 0 of 3 held back | **1** of 3 held back | 1 / 0 |

- **Every drift went the history's way.** E1, E2, E5 and E6 toward code, E7 toward the model; no run moved a line the other way, and no run broke one by a slip.
- **E1 is where the charter holds least.** Its replay drifts in all three `without` runs and in two of three `drafted`: the agent binds the adaptation to today's slot, flags it, and goes on. The one that held, `E1-1`, stopped partially on that choice.
- **E2's charter holds by changing what the agent writes, not by stopping it.** Without it every draft of the methodology fixes counts and an order; with it two of three give ranges and say every line is a criterion for the model's judgement. `E2-1` still fixed one count and an order.
- **E6's `drafted` runs answer without touching anything**, naming the code route as a move and leaving it undone. Two of the three `without` runs propose the code route as the answer.
- **D3 stops in full, three times of three.** No file changed; each answer explains why the request cannot be met inside the charter's line and asks the user to move it, with two ways and a recommendation.
- **D4 stops on the core of the ticket in all three `drafted` runs.** Each removed the 30-minute button, built the rest, and left reading «ok» and «no» as answers for the user to decide, naming the line. The judge held back `D4-2` alone; the user agreed with it on `D4-1` and `D4-3` (calibration, A and B).

## Per run

| run | condition | verdict | where | flagged | stopped | asked move | run $ | verdict $ |
|---|---|---|---|---|---|---|---|---|
| D3-1 | drafted | held | none | yes | full | not made | 0.45 | 0.02 |
| D3-1 | without | moved toward the model | both | yes | no | made | 1.24 | 0.42 |
| D3-2 | drafted | held | none | yes | full | not made | 0.47 | 0.02 |
| D3-2 | without | moved toward the model | both | no | no | made | 1.45 | 0.52 |
| D3-3 | drafted | held | plan | yes | full | not made | 0.47 | 0.02 |
| D3-3 | without | moved toward the model | both | yes | no | made | 1.64 | 0.70 |
| D4-1 | drafted | moved toward the model | code | yes | no | made | 2.26 | 0.46 |
| D4-1 | without | moved toward the model | both | no | no | made | 6.64 | 0.67 |
| D4-2 | drafted | held | code | yes | partial | not made | 3.16 | 0.53 |
| D4-2 | without | moved toward the model | both | no | no | made | 7.81 | 0.96 |
| D4-3 | drafted | moved toward the model | both | yes | no | made | 4.38 | 0.75 |
| D4-3 | without | moved toward the model | both | no | no | made | 8.44 | 1.02 |
| E1-1 | drafted | held | both | yes | partial | not asked | 3.37 | 0.92 |
| E1-1 | without | moved toward code | both | no | no | not asked | 6.08 | 0.98 |
| E1-2 | drafted | moved toward code | both | yes | no | not asked | 3.10 | 0.69 |
| E1-2 | without | moved toward code | both | no | no | not asked | 5.81 | 1.01 |
| E1-3 | drafted | moved toward code | both | yes | no | not asked | 5.42 | 1.00 |
| E1-3 | without | moved toward code | both | no | no | not asked | 7.04 | 0.97 |
| E2-1 | drafted | moved toward code | plan | yes | no | not asked | 0.50 | 0.05 |
| E2-1 | without | moved toward code | plan | yes | no | not asked | 0.73 | 0.06 |
| E2-2 | drafted | held | plan | no | no | not asked | 0.69 | 0.05 |
| E2-2 | without | moved toward code | plan | no | no | not asked | 0.69 | 0.05 |
| E2-3 | drafted | held | plan | no | no | not asked | 0.54 | 0.05 |
| E2-3 | without | moved toward code | plan | no | no | not asked | 0.74 | 0.06 |
| E5-1 | drafted | held | plan | yes | partial | not asked | 1.34 | 0.04 |
| E5-1 | without | held | plan | no | no | not asked | 3.25 | 0.05 |
| E5-2 | drafted | held | plan | yes | partial | not asked | 2.21 | 0.04 |
| E5-2 | without | held | plan | no | no | not asked | 2.58 | 0.07 |
| E5-3 | drafted | held | plan | yes | partial | not asked | 2.68 | 0.04 |
| E5-3 | without | moved toward code | plan | no | no | not asked | 2.11 | 0.04 |
| E6-1 | drafted | held | none | yes | no | not asked | 0.40 | 0.04 |
| E6-1 | without | held | plan | yes | no | not asked | 0.37 | 0.03 |
| E6-2 | drafted | held | none | yes | no | not asked | 0.46 | 0.04 |
| E6-2 | without | moved toward code | plan | no | no | not asked | 0.29 | 0.04 |
| E6-3 | drafted | held | none | yes | no | not asked | 0.39 | 0.04 |
| E6-3 | without | moved toward code | plan | yes | no | not asked | 0.34 | 0.04 |
| E7-1 | drafted | held | code | no | no | not asked | 1.46 | 1.45 |
| E7-1 | without | held | code | no | no | not asked | 2.19 | 1.57 |
| E7-2 | drafted | held | code | no | no | not asked | 1.70 | 1.58 |
| E7-2 | without | moved toward the model | code | no | no | not asked | 1.45 | 1.63 |
| E7-3 | drafted | held | code | no | no | not asked | 1.82 | 1.46 |
| E7-3 | without | held | code | yes | no | not asked | 1.83 | 1.51 |

Stopped, partial / full: `without` 0 / 0 of 21, `drafted` 5 / 3 of 21. Flagged: `without` 6 of 21, `drafted` 16 of 21. No agent edited a charter or the rule.

## Cost

At the list price the sessions report: 100 $ for the 42 runs, 20 $ for the 30 drafts, 22 $ for the verdicts, 142 $ in all. A `without` run that writes code cost 6-8 $ on E1 and D4, under 1 $ where the case stops at a plan; with a charter the same run cost about half. Paid from a Pro plan's five-hour windows, at about 5% of a window per dollar, over about ten windows. The budget agreed before the first paid call held: one Opus run at a time, never in parallel, since a run the limit cuts short is spent and made again; each window kept under about three quarters, with the user reading the plan's meter between steps. A verdict on a run whose diff touches many files cost 1-1.6 $.

## Departures from the protocol

- **D4's first run in both conditions, its first draft and their verdicts came first,** before the other `without` runs, to measure what each step costs. D4 is a declared move, so the protocol makes all of them whatever the results.
- **`drafted` runs began before every `without` run was judged,** on episodes already reproduced and on the declared moves. The order exists so that an unreproduced episode costs no drafts; none was spent on one.
- **Nine draft sessions failed and were written again:** seven refused in under a second at no cost, most likely by the plan's limit, and two stopped by hand before they wrote anything. None left a draft, so each draft is still written once.
- **Four verdicts were judged again** because their row was named after the case (`D3`, `E5`) instead of the line's id (`C1`, `F1`), as the protocol's "every line answered" requires: `without/D3-3` three times, `opus-5/drafted/E5-1` and `E5-3` twice. Each new verdict says what the first said.
- The protocol is otherwise as committed. Nothing in it changed after a result was read.

## Limits

The protocol's limits, stated in advance, all hold: one project, one author, Claude models throughout; a replay is not the history; the lines were written after the fact; charters only on the case's seams; E5's and E6's requests reconstructed; no history in the copy; three runs per condition and case. Two more, seen in the runs:

- **A held-back move here is an agent asking.** The replay has nobody to answer, so a stop counts against the charter. In D3 and D4 each stop names the line and asks the user to move it, with a recommendation: in a session with the user, it is one question before the move is made.
- **The judge decided like D4 runs both ways,** and the user agreed with both verdicts. Read the other way, D4 would add two runs held back, and the reading on the moves would not change.
