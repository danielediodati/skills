# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; [openpoints.md](openpoints.md) holds what is still undecided.

A session is a milestone: it ends with something that can be shown. Its tickets are files under `docs/work/<session>-<name>/issues/`. A closed ticket is deleted and its line here is removed. A closed session becomes one row under *Done*; its tag keeps the details.

## Done

| # | version | shipped |
| --- | --- | --- |
| 1 | `0.1.0` | A table, per request, of where each decision ended up with and without the seam charter, judged blind |
| 2 | `0.2.0` | A real edd run on `triage_ticket`: budget agreed first, core set before extended, verdict against the target |
| 3 | `0.3.0` | The silent drift rate with the rule alone, beside neither and both, and the pre-fixed decision on whether a charter per seam stays mandatory |
| 4 | `0.4.0` | 24 charters drafted from the code by Sonnet and Haiku, read line by line against the user's |
| 5 | `0.5.0` | A README section with Sonnet's silent drift rate, with no charter and with an unread one it wrote, with intervals |
| 6 | `0.6.0` | Haiku's rate beside Sonnet's in the README, each with its intervals |
| 8 | `0.8.0` | The repository public on GitHub, its history rewritten clean, with a README that teaches the plugin through one example |

## Session 7 - `0.7.0` - Would the charter have stopped a drift that really happened?

**Shows**: REPS's drift episodes, each replayed by the model that made it, without a charter and with one, and whether the agent holds the line where the history did not.

Every number before this one comes from four synthetic seams of one file each. REPS is a real project with seams in cascade, built by Opus.

3. **Replay the episodes.** With Opus, 3 runs per condition - [ticket](docs/work/7-real-project/issues/03-replay.md)

## Parked

No session yet.

- **The evals in a repository of their own**, the synthetic seams' and REPS's, after session 7 closes: to grill before it becomes a session. The plugin ships without 7 MB of runs; the evals pin the plugin they measure, and the README points to them.
- Hosts other than Claude Code (version 2).
- Candidate skills: `budget`, `agent-topology`, `failure-triage`, `context-budget`.
- The author's personal `roadmap` skill, outside this repo: support for GitHub Issues, sessions against milestones.
