# a4a

Agents for agents: agentic engineering of agentic systems. Skills appear as `a4a:<skill>`.

## edd: eval-driven development

The TDD loop for behaviour a model produces. Deterministic seams keep going through `tdd`; model seams (prompts, graph nodes, routing, tool choice, retrieval, sub-agents, fine-tunes) go through cases, graders, a baseline and noise-aware decisions. Its central rule stops the drift of agent projects into ETL: a model seam becomes deterministic code only when an eval shows the code scores at least as well, recorded in an ADR.

Claude loads it on its own when work touches model behaviour, or call it explicitly with `/a4a:edd`.

| File | Content |
|---|---|
| `skills/edd/SKILL.md` | the loop, noise floor, held-out split, anti-patterns, hooks into the spec → tickets → implement → review flow |
| `skills/edd/GRADERS.md` | the grader ladder, model judge calibration, trajectory graders |
| `skills/edd/FORMAT.md` | cases, adapter contract, calibration labels, run files, log |
| `skills/edd/scripts/` | `run_evals.py`, `judge.py`, `calibrate.py`: Python standard library only |

## Wiring it into a project

Add this to the project's `CLAUDE.md` (or `AGENTS.md`), so every session and every implementer sub-agent sees it:

```md
## Model behaviour
- Deterministic seams are built with `tdd`; model seams (prompts, graph nodes, routing, tool choice, retrieval, sub-agents) with `edd` from the dd plugin.
- A model seam never becomes deterministic code without an eval showing it scores at least as well, recorded in an ADR.
- Tickets that change a model seam say `Build with: edd`; their acceptance criteria are eval thresholds.
- Eval results live in `evals/log.md`.
```

Then, per project:

```bash
mkdir -p evals && cp <dd>/skills/edd/scripts/*.py evals/
# per seam: evals/<seam>/cases.jsonl, system.py, grader.py (see FORMAT.md)
python evals/run_evals.py <seam> --speed smoke                 # every iteration
python evals/run_evals.py <seam> --note "one change"           # full run, k = 3; the first one is the baseline
python evals/run_evals.py <seam> --promote-last                # keep the change just measured
python evals/run_evals.py <seam> --split heldout --target 0.8  # milestones only
```

The model judge reads `EDD_JUDGE_MODEL`, `EDD_JUDGE_BASE_URL` (default Ollama at `http://localhost:11434/v1`; Groq: `https://api.groq.com/openai/v1`) and `EDD_JUDGE_API_KEY`.

## Install

- **Claude app**: accept the `dd.plugin` file.
- **Claude Code**: `/plugin marketplace add danielediodati/skills`, then `/plugin install a4a@danielediodati`. To try a local copy without installing: `claude --plugin-dir <path to this folder>`.
