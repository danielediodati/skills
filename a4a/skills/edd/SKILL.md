---
name: edd
description: Eval-driven development for a stochastic seam, a point where a model decides (an agent, a router, a prompt, a tool choice, a retrieval, a model judge). Use when such a seam changes: its prompt, its model, its tools, the code around it, or its charter. Measures one change on the seam's eval set and decides it against the charter, the target and the best result. Deterministic code is tested with unit tests instead; a seam with no charter gets one from `charter` first.
---

# Eval-driven development

A **stochastic seam** is a point where a model's output enters the system. Its output varies from run to run, so it is tested with an **eval**: a set of cases run through the seam and scored by graders, repeated to account for noise. This skill runs only when a stochastic seam changes: one change, measured, then kept or reverted.

A deterministic seam (same input, same output) is tested with unit tests written first; this loop is not for it.

## Before the first change

- **Read the charter** at `evals/<seam>/charter.md`: what the model is free to decide, what code constrains, the target. A seam with no charter gets one first, with the user (the `charter` skill). Only the user changes a charter.
- **Find the eval set**: `evals/<seam>/cases.jsonl` and `grader.py`, in the formats of [FORMAT.md](FORMAT.md) and [GRADERS.md](GRADERS.md). A seam with no eval set gets one before it changes. Writing cases and graders is the job of the `eval` skill; until it exists, write them from the charter's eval direction following those two files.

## The line holds

The charter splits the seam's decisions between the model (freedom) and code (constraint). Where there is freedom, freedom stays; where there is a constraint, the constraint stays. Moving the line is a decision, never a side effect of implementation.

- **Before adding a rule in code at a stochastic seam**, ask whether it takes a decision away from the model: a constant, a default, a closed menu, a canned reply, input reshaped before the model reads it. If it does, the way that keeps the freedom is a tool the model can call or feedback it can read. Moving the line is the user's decision.
- **Before handing the model something code owns** (arithmetic, a value that must come from a list, a check), ask the same question the other way round.
- **A change of charter, in either direction, is decided by an eval**: the same cases run on the charter as it is and on the proposed version, both scores go to the user, the user chooses, and the choice is recorded in an ADR. Neither side is the default: freedom adapts to cases nobody foresaw; constraint buys reliability, lower cost, lower latency and an answer that is easy to check.

## The loop

1. **One change.** A prompt, a tool description, the model, the code around the call, a sampling parameter, a retrieval setting. Two changes in one run cannot be attributed.
2. **Core set, then extended set.** The core set runs first; a change that fails it is rejected without spending on the rest. The extended set, the whole eval set, runs only after the core passes, and only it can accept a change.
3. **Verdict.** Below the charter's target: failure, the only one. Below this model's best result by more than the run-to-run spread, at or above the target: a warning in the report, not a failure. The best result informs; the target decides.
4. **Read the losses.** The runner lists by case id the cases the change turned from pass to fail. Keeping the change accepts them; say so to the user.
5. **Read failures.** Read the failing outputs and tag each with a failure category in the case's `tags`. The categories, not the score, choose the next change.
6. **Commit** with the score in the message. The runner has already logged the run.

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

## Where things live

- `evals/<seam>/charter.md`: the seam charter.
- `evals/<seam>/cases.jsonl`, `system.py`, `grader.py`: the eval set, the adapter that runs one case through the seam, the grader. Formats in [FORMAT.md](FORMAT.md).
- `evals/<seam>/calibration.jsonl`: labels for calibrating a model judge ([GRADERS.md](GRADERS.md)).
- `evals/<seam>/runs/`: one file per run, written by the runner.
- `evals/log.md`: one row per run, written by the runner.

If the project has no eval runner, copy the three files in [scripts/](scripts/) into `evals/`; do not write a new runner. They need only the Python standard library: `run_evals.py` runs a seam, `judge.py` is the model judge for any OpenAI-compatible endpoint, `calibrate.py` calibrates it. If the project already uses an eval framework (Inspect, promptfoo, LangSmith), keep it and its formats; every rule above still applies.
