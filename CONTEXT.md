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
| **Seam charter** | The written declaration of one stochastic seam: what is free, what is constrained and why, its target and budget, and the direction for its eval set (the rules the cases and graders will follow, not the cases themselves). Written by the `grill-seam` skill. |
| **Target** | The score a seam has to reach on its eval set. Declared in the charter as a goal before the eval set exists; corrected only by the user's decision once the first run shows the noise floor. |
| **Programmatic drift** | Freedom the design gave to the model being taken over by code, without a decision to move it. The plugin's main target: it is what coding agents do by default. |
| **Substitution** | Programmatic drift where code takes the decision in place of the model: a value fixed in a constant, a canned reply. |
| **Templating** | Programmatic drift where the model still decides, but only by picking from a closed list prepared in advance. |
| **Over-delegation** | The opposite drift: a constraint dissolving into model judgement (the model does arithmetic the code owned, or may invent a value that had to come from a list). |
| **Seam** | The boundary where a module's interface lives and where it is tested. |
| **Deterministic seam** | Same input, same output. Tested with unit tests (TDD). |
| **Stochastic seam** | Output produced by a model: prompt, graph node, routing, tool choice, retrieval, sub-agent, fine-tune. It varies from run to run, so it is tested with evals (EDD). A model call stays a stochastic seam even at temperature 0. The practical test: it has its own eval suite. Usually an agent; sometimes a router, a single prompt or a model judge. The inner steps of an agent are not seams until they are evaluated on their own. |
| **Eval** | A set of cases run through a seam and scored by graders, repeated to account for noise. |
| **Grader** | Scores one output: exact check, rule, or calibrated model judge. |
| **Baseline** | The last promoted eval result; every change is compared against it. |
| **Noise floor** | Run-to-run spread of a seam's score; differences inside it are not improvements. |

## Decisions

1. **One plugin, `a4a`, inside the `danielediodati` marketplace,** scoped to LLM agentic systems. Replaces the earlier plan of one plugin per domain. A second plugin for generic workflow skills was considered and set aside; the marketplace leaves room for it. The author's `roadmap` skill is one of those: it stays personal, outside `a4a`.
2. **No fork of external skill collections.** New skills live here; behaviour of external skills is adapted through wrappers or optional references, never by editing copies.
3. **Standalone first.** No skill may require another collection to work.
4. **Where there is freedom, freedom stays; where there is a constraint, the constraint stays.** How a seam splits between the two is a trade-off decided on purpose, and the solution has to match it. Moving the line is a decision, never a side effect of implementation. Where no line is drawn yet, the plugin favours neither side: it makes the user decide and shows what each side buys (freedom: adapting to unforeseen cases; constraint: reliability, cost, latency, ease of checking). This is the core rule of the plugin.
5. **Scripts use the Python standard library only,** so skills run in any environment without installs.
6. **Few skills per plugin (target 5 to 7).** Overlapping descriptions make the agent load the wrong skill.
7. **Each stochastic seam has a seam charter.** It lives at `evals/<seam>/charter.md`, beside that seam's eval set and baseline, so every skill knows where to find it. It never lives in a ticket: a ticket closes, the seam stays.
8. **Drift is fought at four points, all reading the seam charter:** a design skill writes it; a short rule a setup skill puts in the project's `AGENTS.md` (always in context) sends the coding agent to it before a seam is touched; `edd` builds the seam with the line as given; a review skill compares a diff against it.
9. **An eval has two jobs.** It verifies that a seam, with its charter as written, clears its bar. And it decides a change of charter in either direction: the same cases run on both versions, the scores are compared, and the choice is recorded in an ADR.

## Conventions for skills

- `description` states **when** to use the skill, concretely, and how it differs from the closest neighbour (e.g. "for deterministic code use tdd").
- References to other skills sit in one section per skill, so a rename elsewhere costs one edit.
- Write in English. No em dashes.
- Every skill is tested on a toy project before release; scripts are run end to end.

## Status

| Skill | State |
|---|---|
| `setup-agentic-project` (the `AGENTS.md` rule, the seam inventory) | First draft. Untested. |
| `grill-seam` (writes a seam charter) | First draft. Untested. |
| `eval-set` (cases, graders, judge calibration, first baseline) | Planned. Today part of `edd`. |
| `edd` (eval-driven development: one change, measure, decide) | Built. Needs the symmetric rule, "stochastic seam", and its references to external skills removed. |
| `drift-review` (compares a diff against the charters) | Planned. Today one line in `edd`. |
| `budget`, `agent-topology`, `failure-triage`, `context-budget` | Candidates, after the first five hold. |

The first two are tested on one real seam before the other three are written: if a charter plus the `AGENTS.md` rule does not change what a coding agent does, the rest has nothing to stand on.
