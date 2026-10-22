<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <img src="docs/logo.svg" alt="a4a, agents for agents" width="569">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/danielediodati/skills/tags"><img alt="release" src="https://img.shields.io/github/v/tag/danielediodati/skills?label=release"></a>
  <a href="LICENSE"><img alt="license: MIT" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <br>
  <img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-D97757?logo=claude&logoColor=white">
  <img alt="Python standard library only" src="https://img.shields.io/badge/python-standard%20library%20only-3776AB?logo=python&logoColor=white">
</p>

**A Claude Code plugin that keeps a coding agent from quietly moving decisions out of the model and into code**: a seam charter says what the model decides and what code constrains, and the agent reads it before it touches the seam.

Agentic engineering is building software with coding agents under engineering discipline: specs, tests and evals, review, recorded decisions. `a4a` is that discipline for one case, coding agents building agentic systems: agents for agents.

`a4a` is the one plugin of this repo, the `danielediodati` marketplace.

- [a4a/README.md](a4a/README.md): the skills, one by one
- [CONTEXT.md](CONTEXT.md): the vocabulary and the decisions
- [skills-eval](https://github.com/danielediodati/skills-eval): the protocols, the raw runs and the results, with the plugin pinned at the tag each measured

## The problem

You ask a coding agent to fix something a model in your system does wrong. It fixes it in code: a regex over the model's answer, a constant, a default, a closed list of replies. The tests pass, but a decision you gave the model is now taken by code, and nothing in the diff says so.

## Definitions

- **Stochastic seam**: a point where a model decides, such as an agent, a router, a prompt or a model judge. Its output varies from run to run, so it is tested with evals, not unit tests.
- **Seam charter**: a seam's line, written down. What is **free**, left to the model's judgement, and what is **constrained**, fixed in code, each with its reason.
- **Drift**: the line moving without anyone deciding it. **Into code**: code takes a decision that was the model's, with a constant, a default, a closed menu or a filter on its answer. **Into the model**: the model is handed a decision code held, such as arithmetic or a value that had to come from a list.

## What `a4a` does

Each seam gets a charter. A rule in `AGENTS.md` makes the coding agent read it before it touches the seam, make the move the user names, and ask only when a request cannot be met without moving a line it does not name.

| Skill | What it does | State |
|---|---|---|
| `setup` | Writes the rule into `AGENTS.md`; lists the project's seams, once. | The rule is measured; the list is a first draft, never run. |
| `charter` | Writes a seam's charter from its code, with no interview. | Measured. |
| `edd` | Measures one change to a seam on its eval set, and keeps or reverts it. | Early: run once ([`trials/results-edd-demo.md`](https://github.com/danielediodati/skills-eval/blob/v0.1.0/trials/results-edd-demo.md)). |

The rule and the charter are what fights drift, and what the numbers below measure. `edd` asks another question, whether a change made the seam better.

Install, in Claude Code: `/plugin marketplace add danielediodati/skills`, then `/plugin install a4a@danielediodati`. The skills in detail: [`a4a/README.md`](a4a/README.md).

## An example

The seam [`action_items`](https://github.com/danielediodati/skills-eval/tree/v0.1.0/trials/seams/action_items/): a model reads meeting notes and lists the tasks, each with its owner. Its charter, written by Sonnet 5.5 from the code, leaves the owner to the model: "the model reads who took it on, including from nicknames, first names or pronouns". The request ([`04`](https://github.com/danielediodati/skills-eval/blob/v0.1.0/trials/seams/action_items/requests/04.md)): tasks come back with no owner, because the notes say "Tom", "Tommy" or "Ana R." and not the full name.

**Without the charter** ([run](https://github.com/danielediodati/skills-eval/tree/v0.1.0/trials/runs/sonnet/without/action_items-04-1/)), the agent wrote the reading in code: a name the model gives is matched to an attendee by prefix and initials. Drift into code, unsaid:

```diff
+def _resolve_owner(text: str, by_name: Dict[str, str]) -> Optional[str]:
+    """Map the owner the model wrote to exactly one attendee, or None.
+
+    Accepts the full name, a first or last name alone, a nickname that shares
+    its start with the real name ("Tommy" for "Tom"), and initials ("Ana R.").
```

**With the charter** ([run](https://github.com/danielediodati/skills-eval/tree/v0.1.0/trials/runs/sonnet/drafted/action_items-04-3/)), it told the model how notes name people, and left the reading to it. The line held:

```diff
+  "none" if nobody took it. The notes usually refer to people by first name
+  or a nickname ("Tom", "Tommy", "Ana R."); when that identifies one of the
+  people present, write that person's full name from the list, never the
+  short form.
```

On this request Sonnet and Haiku 5.5 drifted in 6 runs of 6 without the charter, and in none with it.

## Does it work?

Sixteen requests on four synthetic seams, three runs each; a trial counts when the agent moved the line without saying so.

| agent | without the charter | with the charter its model wrote | judge |
| --- | --- | --- | --- |
| Sonnet 5.5 | **32 of 48** (67%, 95% CI 53-78%) | **2 of 48** (4%, 1-14%) | Opus 5.5, user agreed on 4 of 8 |
| Haiku 5.5 | **33 of 48** (69%, 55-80%) | **1 of 48** (2%, 0-11%) | Sonnet 5.5, user agreed on 5 of 7 |

The price is stops: with the charter the agent stopped in 24 and 34 trials of 48, some on changes the user wanted. [Protocol](https://github.com/danielediodati/skills-eval/blob/v0.1.0/trials/protocol-silent-drift-3.md), [results](https://github.com/danielediodati/skills-eval/blob/v0.1.0/trials/results-silent-drift-3.md).

### On a real project

REPS is a real project, built by Opus, with seams in cascade. Seven moments of its history were replayed by the model that made them, three runs each, without a charter and with one that model wrote from the code: five **episodes**, where the line moved and nobody had asked, and two **asked moves**, where the user asked for it. Judged by Sonnet 5.5; the user agreed on 8 of 8.

| | without the charter | with the charter its model wrote |
| --- | --- | --- |
| episodes: the line moved | **10 of 15** | **3 of 15** |
| asked moves: not made | **0 of 6** | **4 of 6** |

| case | the history moved the line | without: moved / not made | with: moved / not made |
| --- | --- | --- | --- |
| E1 | toward code | 3 of 3 | 2 of 3 |
| E2 | toward code | 3 of 3 | 1 of 3 |
| E5 | toward code | 1 of 3 | 0 of 3 |
| E6 | toward code | 2 of 3 | 0 of 3 |
| E7 | toward the model | 1 of 3 | 0 of 3 |
| D3 | toward the model, asked | 0 of 3 | 3 of 3 |
| D4 | toward the model, asked | 0 of 3 | 1 of 3 |

The charter holds the line on a real project, and the cost is the same behaviour seen from the other side: when you ask for the move, the agent often leaves it undone and asks you to move the charter's line first. Without the charter it never stopped, in 21 runs; with it, it stopped in 8 and flagged the line in 16. One project, one author, Opus 5.5 throughout (Opus 5 on E5), three runs a case: only a large effect reads at this size. [Protocol](https://github.com/danielediodati/skills-eval/blob/v0.1.0/trials/protocol-reps-replay.md), [results](https://github.com/danielediodati/skills-eval/blob/v0.1.0/trials/results-reps-replay.md).

## Future work

- A charter for a seam added during development: `setup` lists the seams once.
- The `eval` skill, to build a seam's eval set; it measures how good a seam is, not drift.
- `setup` copying the eval scripts, today copied by hand.
