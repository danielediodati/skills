---
name: edd
description: Eval-driven development for a stochastic seam, a point where a model decides (an agent, a router, a prompt, a tool choice, a retrieval, a model judge). Use when such a seam changes: its prompt, its model, its tools, the code around it, or its charter. Measures one change on the seam's eval set and decides it against the charter, the target and the best result. Deterministic code is tested with unit tests instead; writing a seam's charter is a different skill.
---

# Eval-driven development

A **stochastic seam** is a point where a model's output enters the system. Its output varies from run to run, so it is tested with an **eval**: a set of cases run through the seam and scored by graders, repeated to account for noise. This skill runs only when a stochastic seam changes: one change, measured, then kept or reverted.

A deterministic seam (same input, same output) is tested with unit tests written first; this loop is not for it.

## Before the first change

- **Read the charter** at `evals/<seam>/charter.md`: what the model is free to decide, what code constrains, the budget. A seam with no charter gets one first (see Other skills). Only the user changes a charter.
- **Read the target** at `evals/<seam>/eval.md`, beside the eval set: the score the seam has to reach. A seam with no target gets one from the user before its first run, written there as [FORMAT.md](FORMAT.md) says. Only the user sets or corrects a target.
- **Find the eval set**: `evals/<seam>/cases.jsonl` and `grader.py`, read as [FORMAT.md](FORMAT.md) and [GRADERS.md](GRADERS.md) describe them. A seam with no eval set gets one before it changes; writing it is not this skill's job (see Other skills).

## Nothing paid without approval

Eval runs, model screenings and judge calibrations call paid models. Development spending is a constraint this skill holds; it is a different thing from the budget in a charter, which limits what the seam itself may use at run time.

- **Agree the spending budget first.** Before the first paid call of a ticket, ask the user for one budget, in dollars, for the whole ticket. Record the amount they stated: `python evals/run_evals.py --agree-budget <dollars> --note "<ticket>"`.
- **Free checks before any paid call**: the unit tests of the code around the seam, a dry run of the adapter where it can run without a model call, and `EVAL_SET=cases.jsonl python evals/run_evals.py <seam> --check`, which checks the eval set, imports the adapter and the grader, and prints the estimate and the running total without a call. A paid run that a free check would have stopped is money spent for nothing.
- **Every request for approval shows the running total**, e.g. "core and extended sets at k=3, about $0.40; spent $0.84 of $2.00". Never ask for one run alone, without the total.
- The runner refuses to start a run whose estimate, core and extended sets together, would take the total past the budget; it checks again before the extended set, and logs each run's cost and the total. Raising the budget is the user's decision, asked in one request with the total; recorded with the same `--note`, it keeps what is already spent.
- **Screen models cheapest first.** When several models are tried, the cheapest that could clear the target runs first; a dearer one runs only when the cheaper ones fall short. `--model <name>` hands the model to the adapter, so the model logged is the model called.

**When the budget is spent** and the runs are still below the target with the charter intact, stop. Put the ways out to the user and take none yourself:

- another model: the best results kept per model show whether one already clears the target;
- the line moved on purpose: a charter change, the same cases run on both versions, an ADR;
- a lower target;
- the failure accepted.

Recommend a model change only with its evidence: what was tried on the model's side (prompt, tool descriptions, examples, sampling) and how it failed, by failure category.

## The line holds

The charter splits the seam's decisions between the model (freedom) and code (constraint). Where there is freedom, freedom stays; where there is a constraint, the constraint stays. Moving the line is a decision, never a side effect of implementation.

- **Before adding a rule in code at a stochastic seam**, ask whether it takes a decision away from the model: a constant, a default, a closed menu, a canned reply, input reshaped before the model reads it. If it does, the way that keeps the freedom is a tool the model can call or feedback it can read. Moving the line is the user's decision.
- **Before handing the model something code owns** (arithmetic, a value that must come from a list, a check), ask the same question the other way round.
- **A change of charter, in either direction, is decided by an eval**: the same cases run on the charter as it is and on the proposed version, both scores go to the user, the user chooses, and the choice is recorded in an ADR. Neither side is the default: freedom adapts to cases nobody foresaw; constraint buys reliability, lower cost, lower latency and an answer that is easy to check.

## The loop

1. **One change.** A prompt, a tool description, the model, the code around the call, a sampling parameter, a retrieval setting. Two changes in one run cannot be attributed.
2. **Core set, then extended set.** `EVAL_SET=cases.jsonl python evals/run_evals.py <seam> --note "<the change>"`. The runner reads the target from `evals/<seam>/eval.md`. The core set (the cases marked `core`) runs first; a change whose core score is below the target is rejected without a call spent on the rest. The extended set, every case of the split, runs only after the core passes, and only it can accept a change. The eval set is named in the environment, never by a path in the code.
3. **Verdict.** Below the seam's target: failure, the only one. Below this model's best result by more than the run-to-run spread (the wider of the two runs' spreads), at or above the target: a warning in the report, not a failure, because the highest score is partly a lucky run. The best result informs; the target decides. Best results are kept per model, each with the code version it was measured on: a change to the grader or the eval set discards them all, a change to the code keeps them, reported as measured on an earlier version. A run below the target is recorded and never kept as a best result.
4. **Check the diff against the charter as it was** (next section). It runs whatever the score, and a moved line stops the change.
5. **Read the losses.** The runner lists by case id the cases the change turned from pass to fail. Keeping the change accepts them; say so to the user.
6. **Read failures.** Read the failing outputs in the run file, which keeps what the seam answered on every run, and tag each with a failure category in the case's `tags`. Tags describe a case and do not change it: editing them discards no best result. The categories, not the score, choose the next change.
7. **Commit** with the score in the message. The runner has already logged the run.

## The diff against the charter

Before a change is accepted, read its diff against the seam's charter **as it was before the change**: `git show <base>:evals/<seam>/charter.md`, where `<base>` is the commit the change started from. Never the charter in the working tree: a change that moved a line can rewrite the charter in the same diff. A diff that edits the charter is itself a finding: only the user changes a charter.

For each hunk that touches the seam (the prompt, the code that builds the model's input, the code that reads its answer, the constants and defaults around them):

1. **Name the decision** the hunk touches, and find its line in the charter.
2. **A free line now taken by code** is drift: a constant or a default in place of the model's choice (substitution), a closed menu the model picks from in place of its own answer (templating), or a prompt that dictates the answer. A criterion in the prompt that the model still applies by reading each input (a definition, a requirement the user stated) informs its judgement and is not a move.
3. **A constrained line now left to the model** is drift the other way (over-delegation): the model does arithmetic code owned, may invent a value that had to come from a list, or a check is loosened.
4. **Look for the three moves agents do not see as moves**, each found in session 1 trials where the agent changed the code without flagging a line:
   - **Input cleaned by code before the model reads it**: quoted text stripped, fields dropped, text normalised. The model no longer decides about what it cannot see, so a free line moved toward code even though the prompt is untouched.
   - **A parsing rule that also catches a free field**: a check written for one field rejects or rewrites another field the model owns.
   - **A missing field defaulted instead of refused**: a constraint that says "refuse" or "raise" now lets a value nobody decided through.
5. **Report each move**: the charter line, the hunk that moves it, and the direction (toward code, toward the model). A hunk that brings the code back to what the charter says is not a move; say so. A change that moves no line says so in one line.

A moved line stops the change, whatever the score: name the line, say what moving it would buy, and leave the decision to the user. A score cannot clear this check: it measures whether the output is good, not who took the decision, so a free decision turned into a constant can raise the score and still be drift.

## Noise floor

Models are stochastic. Run each case `k` times (default 3, always odd) at the sampling settings used in production. The **score** is the mean, over the `k` runs, of the fraction of cases passed; the **spread** is the lowest to highest of those `k` fractions. A case passes when the majority of its runs pass. Differences inside the spread are not improvements.

With `n` cases one case is worth `100/n` points: on 20 cases a 5-point gain is a single flipped case, a hint, not a result. The runner pairs runs case by case and gives a one-sided sign test on gains against losses; a gain with p above 0.05 is provisional until more cases or a larger `k` confirm it.

The model, the provider and the quantization are part of the result: a score measured on one transfers to another only after a run there.

## Held-out split

Dev and held-out are the two splits of an eval set, a different axis from core and extended. Tune on **dev**; run **heldout** and read its failures only at milestones, so its score is not a memory of the cases. When held-out failures have been read often enough to steer changes, move those cases into dev and draw fresh held-out cases (a redefinition of the eval set, recorded in an ADR).

## Failure categories

Derive each seam's categories from its first failures and keep them few (3 to 7). For multi-agent systems, seed them from the MAST taxonomy: **specification** (a role or task misread or underspecified), **inter-agent misalignment** (lost context, ignored input, conflicting actions), **verification** (a result declared done without checking, or checked wrongly).

## Anti-patterns

- **Vibe check**: judging a change by reading a couple of outputs. The tell: no number in the commit.
- **Teaching to the test**: editing prompts to fix named held-out cases.
- **Moving goalposts**: changing the grader or the eval set in the same run as the seam. Either change discards the seam's best results, because scores before and after no longer compare; it is a redefinition, recorded in an ADR.
- **Tautological grader**: a reference produced by the system itself, or a judge sharing the system's model and prompt.
- **Programmatic drift**: a free decision taken over by code to make the score rise or a check pass. A score measures whether the output is good, not who took the decision.
- **Averaging away**: reading only the total when a tag regresses. The runner reports per-tag scores; read them.

## Other skills

- `charter` writes a seam's charter from its code, and amends it when the user moves a line.
- `eval` will write a seam's eval set: cases, graders, judge calibration, the core and extended sets. Until it exists, [FORMAT.md](FORMAT.md) and [GRADERS.md](GRADERS.md) are where the eval set's rules stand, and `evals/<seam>/eval.md` holds its target and direction.
- `setup` writes the rule a project's `AGENTS.md` carries for stochastic seams and spending.

## Where things live

- `evals/<seam>/charter.md`: the seam charter.
- `evals/<seam>/eval.md`: the seam's target and the direction of its eval set.
- `evals/<seam>/cases.jsonl`, `system.py`, `grader.py`: the eval set, the adapter that runs one case through the seam, the grader. Formats in [FORMAT.md](FORMAT.md).
- `evals/<seam>/calibration.jsonl`: labels for calibrating a model judge ([GRADERS.md](GRADERS.md)).
- `evals/<seam>/runs/`: one file per run, written by the runner.
- `evals/<seam>/best.json`: the best result of each model, written by the runner.
- `evals/log.md`: one row per run, written by the runner.

If the project has no eval runner, copy the three files in [scripts/](scripts/) into `evals/`; do not write a new runner. They need only the Python standard library: `run_evals.py` runs a seam, `judge.py` is the model judge for any OpenAI-compatible endpoint, `calibrate.py` calibrates it. If the project already uses an eval framework (Inspect, promptfoo, LangSmith), keep it and its formats; every rule above still applies.
