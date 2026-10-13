# a4a

Agents for agents: agentic engineering of agentic systems. Skills appear as `a4a:<skill>`.

A coding agent working on a system where a model decides tends to move decisions out of the model and into code: a constant, a default, a closed menu, a canned reply. The plugin keeps each decision where you put it. Every **stochastic seam** (a point where a model decides: an agent, a router, a prompt, a model judge) gets a **seam charter** that says what the model is free to decide and what code constrains; the coding agent reads it before touching the seam, and every change is measured against it.

| Skill | When |
|---|---|
| `setup` | Once per project: writes the rule into `AGENTS.md` and lists the stochastic seams, with or without a charter. Call it with `/a4a:setup`. |
| `charter` | When a seam has no charter, or you move its line between freedom and constraint. The agent writes it from the seam's code, with no interview. |
| `edd` | When a stochastic seam changes: one change, measured on the seam's eval set, decided against the charter, the target and the best result. |

## edd: eval-driven development

| File | Content |
|---|---|
| `skills/edd/SKILL.md` | the loop, the line, noise floor, held-out split, anti-patterns |
| `skills/edd/GRADERS.md` | the grader ladder, model judge calibration, trajectory graders |
| `skills/edd/FORMAT.md` | cases, adapter contract, calibration labels, run files, log |
| `skills/edd/scripts/` | `run_evals.py`, `judge.py`, `calibrate.py`: Python standard library only |

Per project:

```bash
mkdir -p evals && cp <a4a>/skills/edd/scripts/*.py evals/
# per seam: evals/<seam>/charter.md, eval.md, cases.jsonl, system.py, grader.py (see FORMAT.md)
python evals/run_evals.py --agree-budget 2.00 --note "ticket 12"        # the budget the user agreed
EVAL_SET=cases.jsonl python evals/run_evals.py <seam> --check            # free: checks and the estimate
EVAL_SET=cases.jsonl python evals/run_evals.py <seam> --note "one change"                # the target is in eval.md
```

Nothing paid runs without approval: the runner refuses a run that would take the total past the agreed budget, and every run reports what it cost and the running total.

The model judge reads `EDD_JUDGE_MODEL`, `EDD_JUDGE_BASE_URL` (default Ollama at `http://localhost:11434/v1`; Groq: `https://api.groq.com/openai/v1`) and `EDD_JUDGE_API_KEY`.

### A real run

On the seam `triage_ticket` (a support ticket routed to a queue, with an urgency and a summary), with $2.00 agreed and a target of 0.90 on 17 cases, Haiku 5.5:

| run | change | core | extended | against the target | cost |
|---|---|---|---|---|---|
| 1 | the seam as it is | 1.00 | 0.82 | not met | $0.006 |
| 2 | body cap raised from 2000 to 8000 characters | 1.00 | 0.92 | met | $0.004 |

Each run was approved with its estimate and the running total; the loop stopped at the target with $0.01 spent. The one case still failing needs a line of the charter moved, so it went to the user and was not fixed. The transcript is in [`trials/results-edd-demo.md`](../trials/results-edd-demo.md).

## Install

In Claude Code: `/plugin marketplace add danielediodati/skills`, then `/plugin install a4a@danielediodati`. To try a local copy without installing: `claude --plugin-dir <path to this folder>`.
