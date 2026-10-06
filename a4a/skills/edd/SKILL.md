---
name: edd
description: Eval-driven development, TDD for model behaviour. Use when building or changing anything whose output comes from a model (a prompt, an agent or graph node, a routing decision, a tool choice or tool description, a sub-agent, a RAG step, a fine-tune or adapter), when writing a spec, tickets or acceptance criteria that describe model behaviour, when comparing models, providers or configurations, or when about to replace model behaviour with deterministic code so it can be unit-tested.
---

# Eval-Driven Development

EDD is the red → green loop for behaviour a model produces. A unit test asserts one deterministic output. An **eval** runs a set of **cases** through the system and scores each output with a **grader**, because the same input can produce different outputs and "correct" is often a judgement. This skill is the reference that makes that loop produce numbers worth trusting, and keeps a model-based system from collapsing into deterministic plumbing.

When exploring the codebase, read `GLOSSARY.md` (if it exists) so seam and case names match the domain language, and respect ADRs in the area you're touching.

## Two kinds of seam

A **seam** is where a module's interface lives, the boundary you test at (vocabulary from the `codebase-design` skill, as used by `tdd`). In a system with models, every feature has two kinds:

- A **deterministic seam** has an expected value you can write as a literal before running anything: parsing, schemas, state transitions, constraint checks, a tool's contract. Build these with the `tdd` skill.
- A **model seam** is where a model's output enters the system: a node's response, a routing decision, a tool choice, a plan, a retrieval, a final answer, a whole trajectory. Its expected value needs a reference, a tolerance or a rubric. Build these with this loop.

Before building, write the **seam inventory**: each model seam with its **target**, a number on an eval set ("held-out pass rate ≥ 0.80"), plus a **budget** wherever the system has one ("≤ 20 tool calls", "≤ 6 minutes per task", "fits a 32k context"). Confirm seams, targets and budgets with the user.

## Model seams stay model seams

An assert is easier to write than an eval, so the pull is always to turn model seams into code: a regex instead of intent detection, a lookup table instead of a plan, a fixed pipeline instead of a routing decision. Repeated, that turns an agent into ETL with an LLM call in the middle, and the system loses the judgement it was built for.

The rule: a model seam becomes deterministic code only when an eval shows the deterministic version scores at least as well on the same eval set, beyond the noise floor. The swap gets an ADR carrying both numbers.

Two things are deterministic by design and need no eval: work with a literal answer (validation, formatting, arithmetic, I/O), and **hard constraints** (safety limits, permissions, budgets). A hard constraint checks the model's output and rejects or retries it; the decision stays with the model.

## The loop

1. **Cases first.** Write eval cases before touching the seam. Sources, most valuable first: real failures (traces, logs, bug reports), the spec's acceptance criteria, edge cases from grilling, adversarial inputs. Start with 10 to 30. Done when every acceptance criterion describing model behaviour maps to at least one case.
2. **Grader.** Give each case the cheapest grader that can disagree with the system; [GRADERS.md](GRADERS.md) has the ladder and the calibration procedure for model judges. Done when every case has a grader and every model judge has passed calibration.
3. **Baseline.** Run the full eval set on current behaviour; the first full run of a split becomes its baseline. For a new seam, the baseline is the simplest thing that could work: one prompt, one call, no graph. Done when the log has a baseline row for this commit.
4. **One change.** Change one thing per run: a prompt, a tool description, the model, the graph topology, a sampling parameter, a retrieval setting. Two changes in one run cannot be attributed.
5. **Decide.** Keep the change only if (a) the new score is beyond the noise floor of the baseline (next section), and (b) you accept every loss the runner lists by case id. Then promote the run to baseline (`run_evals.py <seam> --promote-last`); otherwise revert. The loop is **green** when the target is met on the held-out split, within budget.
6. **Read failures.** After every run, read the failing outputs and tag each with a failure category in the case's `tags`. The categories, not the score, choose the next change.
7. **Log.** The runner appends the run to `evals/log.md`; put the score in the commit message.

## Noise floor

Models are stochastic. Run each case `k` times (default 3, always odd) at the sampling settings used in production. The **score** is the mean, over the `k` runs, of the fraction of cases passed; the **spread** is the lowest to highest of those `k` fractions. A case passes when the majority of its runs pass. A new score is **beyond noise** when it exceeds the highest single-run score of the baseline.

Compare runs **paired**, case by case against the baseline: **gains** (fail → pass) and **losses** (pass → fail). The runner lists both by case id with a one-sided sign test. With `n` cases one case is worth `100/n` points: on 20 cases a 5-point gain is a single flipped case, a hint, not a result. A gain with sign-test p above 0.05 can be kept, but mark it provisional in the notes and confirm it at the next milestone with more cases or a larger `k`.

Evals cost model calls, so they run at two speeds:

- **Smoke**: the cases marked `smoke` (5 to 10 dev cases), `k = 1`, on every iteration. Smoke runs steer; they never decide.
- **Full**: every case in the split, `k` runs, for every baseline and every decision.

The model, the provider and the quantization are part of the result: a score measured on one transfers to another only after a run there. Log them on every row, with the cost per case (tokens, seconds) whenever the system has a budget.

## Held-out split

Tune on **dev**; report on **heldout**, and read held-out failures only at milestones. Split along the axis the system will meet in production (a new user, a new repository, a new domain), so the held-out score predicts that encounter instead of rewarding memory of the dev cases. When the held-out failures have been read often enough to steer changes, move those cases into dev and draw fresh held-out cases.

## Failure categories

Derive each seam's categories from its first failures and keep them few (3 to 7). For multi-agent systems, seed them from the MAST taxonomy and split them as the data demands: **specification** (a role or task misread or underspecified), **inter-agent misalignment** (lost context, ignored input, conflicting actions between agents), **verification** (a result declared done without checking, or checked wrongly).

## Anti-patterns

- **Vibe check**: judging a change by reading a couple of outputs. The tell: no number in the commit.
- **Teaching to the test**: editing prompts to fix named held-out cases. The tell: the held-out score rises while new real failures look like the old ones.
- **Moving goalposts**: changing grader and system in the same run. A grader change gets its own run against the unchanged system, promoted to baseline, before the next system change; the runner warns when the grader changed since the baseline.
- **Tautological grader**: a reference produced by the system itself, or a judge sharing the system's model and prompt. References come from an independent source: a person, the spec, an executed result, a stronger model checked by a person.
- **Mechanizing for testability**: replacing a model seam with code to make an assert pass, without the eval and the ADR that earn the swap.
- **Averaging away**: reading only the total when a tag regresses. The runner reports per-tag scores; read them.

## Where things live

- `evals/<seam>/cases.jsonl`: the cases, format in [FORMAT.md](FORMAT.md).
- `evals/<seam>/system.py` and `evals/<seam>/grader.py`: the adapter that runs one case through the system, and the grader, versioned with the cases. Contract in [FORMAT.md](FORMAT.md).
- `evals/<seam>/calibration.jsonl`: your labels for calibrating a model judge.
- `evals/<seam>/runs/`: one file per run, written by the runner, read for paired comparison.
- `evals/log.md`: one row per run, written by the runner.

If the project has no eval runner, copy the three files in [scripts/](scripts/) into `evals/` and wire `run_evals.py` into the project's task runner; do not write a new runner. They need only the Python standard library: `run_evals.py` runs a seam, `judge.py` is the rung-4 model judge for any OpenAI-compatible endpoint (Ollama, Groq, vLLM, OpenRouter), `calibrate.py` calibrates it. If the project already uses an eval framework (Inspect, promptfoo, LangSmith), keep it and its formats; every rule above still applies.

## With the rest of the flow

These hooks fit the spec → tickets → implement → review flow (`to-spec`, `to-tickets`, `implement`, `implement-spec`, `code-review`):

- **Spec**: Testing Decisions lists the seam inventory: each model seam with its eval set, grader rung, target and budget.
- **Tickets**: building a seam's eval set (cases, grader, judge calibration, baseline) is its own ticket, and it blocks every ticket that changes that seam. Each ticket that changes a model seam states `Build with: edd` in its body, and its acceptance criteria are eval thresholds ("planner held-out score ≥ 0.80 at k = 3, no unaccepted loss").
- **Implementation**: deterministic seams through `tdd`, model seams through this loop. An implementer that would call `tdd` on a ticket marked `Build with: edd` uses this skill instead.
- **Review**: on the Spec axis, a change to a model seam without eval numbers is a finding, and so is a model seam from the inventory that became deterministic code without an ADR.