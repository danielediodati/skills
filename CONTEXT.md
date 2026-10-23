# CONTEXT

Skills for disciplined agentic engineering of AI systems.

This file is the shared context for anyone (human or coding agent) working on this repo. Read it before adding or changing a skill.

## Purpose

A collection of agent skills for engineering LLM agentic systems with coding agents. Deep learning (training, inference) is out of scope. The skills target the places where coding agents go wrong by default on AI work: non-determinism, evals that measure the wrong thing, data leakage, silent cost growth, model behaviour quietly replaced by deterministic code.

**Agentic engineering** here means the development methodology: working with coding agents under engineering discipline (specs, tests and evals, review, recorded decisions) rather than accepting whatever the agent produces. On its own it does not mean "engineering of agents": generic skill collections cover the method for any software. This repo covers one application of it, **agentic engineering of agents**: coding agents building systems where a model decides. Hence the plugin's name, `a4a`, agents for agents.

## Positioning

- **Standalone.** Every skill works on its own, with no dependency on any other skill collection.
- **No cross-references.** A skill does not name skills from other collections. Where another discipline applies (e.g. test-first for a deterministic seam) the skill states the rule in a line and moves on. Collections that inspired this one are credited in the README only.
- **Specific over broad.** Each skill stays narrow. A skill earns its place only if it changes what the agent would do without it.
- **Model agnostic, twice.** The skills work whichever model runs the coding agent, and the evals they produce are not tied to the provider of the model inside the system under development.
- **Host: Claude Code first.** Version 1 ships as a Claude Code plugin. Other hosts come in version 2.
- **Public.** Written to be published and used by others.

## Structure

The repo is the `danielediodati` marketplace. It holds one plugin, `a4a` (agents for agents), a stack of several skills that appear as `a4a:<skill>`.

```
.claude-plugin/marketplace.json
a4a/.claude-plugin/plugin.json
a4a/skills/<skill>/SKILL.md
```
 Skill bodies stay portable: a Claude Code feature (subagents, hooks, command arguments) is only ever an optional speed-up, and every skill works without it.

## Glossary

| Term | Meaning |
|---|---|
| **Skill** | A folder with a `SKILL.md` (frontmatter `name`, `description`) plus optional reference files and scripts. |
| **Plugin** | The installable bundle of this repo's skills. |
| **Freedom** | What a seam leaves to the model's judgement. |
| **Constraint** | What a seam fixes in code: what is allowed, in what order, within what limits. |
| **Atomic seam** | A stochastic seam taken alone: one point where a model decides, with the code around it. Opposed to seams in cascade, where one seam's output feeds the next. The plugin is tested on atomic seams first. |
| **Seam charter** | The written declaration of one stochastic seam: what is free, what is constrained and why, and its budget. The `charter` skill has the coding agent write it alone, from the seam's code as it is; a line moves only when the user names the move in a request (decision 15). |
| **Target** | The score a seam has to reach on its eval set. Declared as a goal in `evals/<seam>/eval.md`, beside the eval set and outside the charter; corrected only by the user's decision once the first run shows the noise floor. A run below the target is a failure, and the only failure. |
| **Programmatic drift** | Freedom the design gave to the model being taken over by code, without a decision to move it. The plugin's main target: it is what coding agents do by default. |
| **Substitution** | Programmatic drift where code takes the decision in place of the model: a value fixed in a constant, a canned reply. |
| **Templating** | Programmatic drift where the model still decides, but only by picking from a closed list prepared in advance. |
| **Over-delegation** | The opposite drift: a constraint dissolving into model judgement (the model does arithmetic the code owned, or may invent a value that had to come from a list). |
| **Drift episode** | Drift as it happens in a real project's history: the run of commits from the last state where a decision sat where the design put it to the first state where it sits on the other side, with the requests that led there. Rarely one commit: each step looks harmless alone. A drift written in a plan (a spec, a ticket, a draft, a proposal) and stopped by the user before any code counts too: only the user's review kept it out, at a cost in time. A move is a decision, kept for contrast, only when the user made it or accepted and kept it; a move the agent wrote down and the user corrected is drift. |
| **Seam** | The boundary where a module's interface lives and where it is tested. |
| **Deterministic seam** | Same input, same output. Tested with unit tests (TDD). |
| **Stochastic seam** | Output produced by a model: prompt, graph node, routing, tool choice, retrieval, sub-agent, fine-tune. It varies from run to run, so it is tested with evals (EDD). A model call stays a stochastic seam even at temperature 0. The practical test: it has its own eval suite. Usually an agent; sometimes a router, a single prompt or a model judge. The inner steps of an agent are not seams until they are evaluated on their own. |
| **Eval** | A set of cases run through a seam and scored by graders, repeated to account for noise. |
| **Core set** | The small part of a seam's eval set that runs first on every change. A change that fails the core set is rejected without spending on the rest. |
| **Extended set** | The whole eval set of a seam. It runs only after the core set passes, and only it can accept a change. |
| **Dev and held-out** | The two splits of an eval set. Dev cases are worked on; held-out cases are read only at milestones, so their score is not a memory of the cases. A different axis from core and extended, which say how many cases run and in what order. |
| **Grader** | Scores one output: exact check, rule, or calibrated model judge. |
| **Result** | One score, identified by four things: the seam's code, the eval set, the grader and the model. The four identify a measurement, not the seam: the seam is what lasts, with its name and charter, while the code under it changes. |
| **Best result** | The highest result at or above the target a model has reached on a seam's eval set, kept for every model with the code version it was measured on. Given in every run's report; a run below it raises a warning, not a failure. Replaces the term "baseline". |
| **Spending budget** | The money a ticket may spend on paid model calls while the system is developed: eval runs, trials, model screenings. Agreed with the user before the first paid call. Distinct from the budget in a seam charter, which limits what the seam itself may use at run time. |
| **Noise floor** | Run-to-run spread of a seam's score; differences inside it are not improvements. |

## Decisions

1. **One plugin, `a4a`, inside the `danielediodati` marketplace,** scoped to LLM agentic systems. Replaces the earlier plan of one plugin per domain. A second plugin for generic workflow skills was considered and set aside; the marketplace leaves room for it. The author's `roadmap` skill is one of those: it stays personal, outside `a4a`.
2. **No fork of external skill collections.** New skills live here.
3. **Standalone first.** No skill may require another collection to work.
4. **Where there is freedom, freedom stays; where there is a constraint, the constraint stays.** How a seam splits between the two is a trade-off decided on purpose, and the solution has to match it. Moving the line is a decision, never a side effect of implementation. Neither side is the default: freedom buys adapting to unforeseen cases; constraint buys reliability, cost, latency, ease of checking. This is the core rule of the plugin; why it runs both ways, and not only against code taking over, is in [ADR 1](docs/adr/0001-freedom-and-constraint-held-symmetrically.md).
5. **Scripts use the Python standard library only,** so skills run in any environment without installs.
6. **Few skills per plugin (target 5 to 7).** Overlapping descriptions make the agent load the wrong skill.
7. **Each stochastic seam has a seam charter.** It lives at `evals/<seam>/charter.md`, beside that seam's eval set and best results, so every skill knows where to find it. It never lives in a ticket: a ticket closes, the seam stays. The coding agent writes it alone, from the code as it is, and asks the user nothing: what the code does not show (a behaviour that is a defect, a field left unchecked on purpose, a limit that is fixed) is settled by the user's request when one touches it. In session 3 a charter written alone drifted in 2 of 24 trials, against 15 with none and 0 with the user's ([`trials/results-auto-charter.md`](https://github.com/danielediodati/skills-eval/blob/v0.1.0/trials/results-auto-charter.md)). It holds three parts: free, constrained, budget. The target and the eval direction live beside it in `eval.md`, until the `eval` skill owns them.
8. **Drift is fought at three points, all reading the seam charter:** `charter` writes it; the rule `setup` puts in the project's `AGENTS.md` (always in context) sends the coding agent to it before a seam is touched; `edd`, before it accepts a change, checks the diff against it. That last check is not a number: a score measures whether the output is good, not who took the decision, so a free decision turned into a constant can raise the score and still be drift.
9. **An eval has two jobs.** It verifies that a seam, with its charter as written, clears its bar. And it decides a change of charter in either direction: the same cases run on both versions, the scores are compared, and the choice is recorded in an ADR.
10. **An eval set is written once per seam and then holds still.** The `eval` skill runs when a seam is new, and calls the eval set finished only when its cases cover every line of the charter and each grader has been seen to fail an output. Redefining an existing eval set (removing or rewriting cases, changing a grader) is a decision recorded in an ADR, so that scores before and after stay comparable and the bar cannot move quietly. Adding a case born from a real failure is not a redefinition: it is logged with the run and needs no ADR, because it can only make the bar harder to clear.
11. **Four skills, named for what they produce, in order of use:** `setup`, `charter`, `eval`, `edd`. `edd` runs only when a stochastic seam changes: the core set first, the extended set only if the core passes.
12. **A run has two lines to hold, and only one can fail it.** Below the seam's target: failure. Below that model's best result but at or above the target: a warning in the report, raised only when the gap is larger than the run-to-run spread, because the highest score is partly a lucky run. The best result informs; the target decides.
13. **The grader and the eval set invalidate, the code ages, the model distinguishes.** A change to the grader or the eval set discards every best result of that seam: the measure changed, so earlier and later scores do not compare. A case's tags are not such a change: they describe the case. A change to the seam's code keeps them, marked as measured on an earlier version: for the same model they are the reference the warning needs, and between models they are reported as out of date until that model is run again. The model is the key the best results are kept by. A charter change discards nothing by itself: when it matters, cases or a grader change with it, and those discard.
14. **Development spending is a constraint the plugin holds.** Nothing paid runs without the user's approval. A spending budget is agreed for the whole ticket first; every later request for approval shows the running total; free local checks run before any paid call; models are screened cheapest first. The incident behind it: one ticket spent about $8 through small approvals with the total never shown, $1.14 of it on a screening a free local check would have caught.
15. **A request settles the line it asks about.** When the user asks for a behaviour the charter rules out, the request is the decision: the coding agent amends that line, makes the change and says so, without stopping to ask. A result asked for and reached by moving a line the request did not name is drift, and the charter holds it: "tasks come back with no owner" asks for owners, not for names matched in code. The move counts as asked only when the user names it: a ticket, plan or draft an agent wrote does not, even once approved, since a move written there is how REPS's E5 drifted. When the request cannot be met at all without moving a line it did not name, the agent asks before it moves it; when moving it is only easier or better, the line stays and nothing is asked. Before this, the rule made the agent stop on every asked move: 4 of 6 on REPS's declared moves ([`trials/results-reps-replay.md`](https://github.com/danielediodati/skills-eval/blob/v0.1.0/trials/results-reps-replay.md)), and on requests whose draft stated today's behaviour as wanted (sessions 5 and 6).
16. **Skills state the general rule; the cases trials find stay in the rubrics.** A drift a trial turns up does not become a line of a skill or of the rule: the rule says what a move is, not which moves agents miss. A list of observed cases in a skill grows with every trial, steers the agent toward what was measured, and changes what earlier trials measured. The rubrics that judge the trials name them, since there they measure and do not guide. Decided while charting the way to 1.0: the rule does not name the four moves agents do not see as moves, and `edd`'s diff check stops naming three of them.

## Known limits

Weak spots that are standing limits, not work to do.

- **Spotting drift in a diff takes judgement.** Telling a legitimate constraint (a closed list of valid ids) from templating (a closed list of styles) is not mechanical, and false alarms would get the check ignored.
- **A charter can go stale.** If the line moves on purpose and the charter is not amended in the same change, the charter becomes the wrong thing.
- **The vocabulary is heavy.** Seam, stochastic seam, charter, drift, substitution, templating, over-delegation, target, noise floor.
- **Over-delegation has one real episode behind it, an omission.** A library default left a schema unenforced in REPS ([`trials/reps/`](https://github.com/danielediodati/skills-eval/tree/v0.1.0/trials/reps/), E7); nobody chose the move. Substitution and templating were derived from one project's documents and confirmed in passing.
- **The process is heavy for a small project.** A charter, an eval set and the loop for every seam is a lot. The charter is cheap, and the agent writes it alone; the eval set is not.

## Conventions for skills

- `description` states **when** to use the skill, concretely, and how it differs from the closest neighbour (e.g. "for deterministic code use tdd").
- References to other skills sit in one section per skill, so a rename elsewhere costs one edit.
- Write in English. No em dashes.
- Every skill is tested on a toy project before release; scripts are run end to end.

## Status

| Skill | State |
|---|---|
| `setup` (the `AGENTS.md` rule, the seam inventory) | First draft. Untested. |
| `charter` (the agent writes a seam charter from the code, alone) | Rewritten in session 3 on the brief its trials measured. |
| `eval` (cases, graders, judge calibration; core and extended sets). Called for a new seam, or to redefine an eval set. | Planned. Today part of `edd`. |
| `edd` (eval-driven development: one change, measure, decide; runs only when a stochastic seam changes) | Rewritten on this file in session 2. Run once, on `triage_ticket` ([`trials/results-edd-demo.md`](https://github.com/danielediodati/skills-eval/blob/v0.1.0/trials/results-edd-demo.md)). |
| `budget`, `agent-topology`, `failure-triage`, `context-budget` | Candidates, after the first four hold. |

A separate skill to verify an eval set, and one to review a diff for drift, were considered and dropped as not central.

The first two are tested on one real seam before the other two are written: if a charter plus the `AGENTS.md` rule does not change what a coding agent does, the rest has nothing to stand on.
