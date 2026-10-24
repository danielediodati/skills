# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; the map in [docs/work/map-drift-protection](docs/work/map-drift-protection/map.md) holds the decisions still open.

A milestone is a release, declared before it is built, and the only thing that ships a version and a tag; a large one starts as a map. A feature is a result that can be shown, described by its spec at `docs/work/<m>.<f>-<name>/spec.md`, and ships no tag. Milestones are numbered in order after the sessions under *Done*, features inside their milestone, tickets inside their feature: ticket `12.1.3` is the third of feature 12.1. Its tickets are files under `docs/work/<m>.<f>-<name>/issues/`; a closed ticket is deleted and its line here is removed. A closed feature becomes one line under its milestone; a closed milestone becomes one row under *Done*, and its tag keeps the details.

## Done

Until milestones, each row was a session: a feature and a version at once.

| # | version | shipped |
| --- | --- | --- |
| 1 | `0.1.0` | A table, per request, of where each decision ended up with and without the seam charter, judged blind |
| 2 | `0.2.0` | A real edd run on `triage_ticket`: budget agreed first, core set before extended, verdict against the target |
| 3 | `0.3.0` | The silent drift rate with the rule alone, beside neither and both, and the pre-fixed decision on whether a charter per seam stays mandatory |
| 4 | `0.4.0` | 24 charters drafted from the code by Sonnet and Haiku, read line by line against the user's |
| 5 | `0.5.0` | A README section with Sonnet's silent drift rate, with no charter and with an unread one it wrote, with intervals |
| 6 | `0.6.0` | Haiku's rate beside Sonnet's in the README, each with its intervals |
| 8 | `0.8.0` | The repository public on GitHub, its history rewritten clean, with a README that teaches the plugin through one example |
| 7 | `0.9.0` | REPS's drift replayed by the model that made it: with a charter, 3 of 15 episodes drift against 10 of 15, and 4 of 6 asked moves are held back against 0 of 6, in the README |
| 9 | `0.10.0` | The trials in `skills-eval`, with their history and the plugin pinned as a submodule; this repository ships without a run |
| 11 | `0.11.0` | The rule, `charter` and `edd` on decision 15: the move the user names is made and flagged, a move only an approved ticket wrote is not, and `charter` asks nothing |

## Milestone 12 - `1.0.0` - Drift protection that holds

**Shows**: `setup`, `charter` and `edd` agreeing with each other and with `CONTEXT.md`, a seam created during development getting its charter, and the final text measured in `skills-eval` holding on REPS's cases and on the synthetic seams.

Its features come from the decisions of [the map](docs/work/map-drift-protection/map.md); none is specified yet.

## Parked

- The `eval` skill, and `setup` copying the eval scripts and creating `evals/`: the next map, once drift protection holds.
- Hosts other than Claude Code (version 2).
- Candidate skills: `budget`, `agent-topology`, `failure-triage`, `context-budget`.
- The author's personal `roadmap` skill, outside this repo: support for GitHub Issues, milestones as GitHub milestones.
