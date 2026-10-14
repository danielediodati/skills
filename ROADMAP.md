# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; [openpoints.md](openpoints.md) holds what is still undecided.

A session is a milestone: it ends with something that can be shown. Its tickets are files under `docs/work/<session>-<name>/issues/`. A closed ticket is deleted and its line here is removed.

## Session 1 - `0.1.0` - Does a charter change what a coding agent does?

**Shows**: a table, per request, of where each decision ended up with and without the seam charter, judged blind to the condition.

The plugin rests on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does when it works on a stochastic seam. This session tests it on atomic seams before any further skill is written. If ticket 5 finds drift in fewer than 12 of its 36 trials without a charter, the problem is residual and the session stops there.

## Session 6 - `0.6.0` - And a charter Haiku wrote, its own?

**Shows**: the README section with Haiku's rate beside Sonnet's, each with its intervals, never compared with each other.

The same protocol with Haiku as agent and writer of its charters, judged by Sonnet. Haiku, not Opus: the user set Opus aside as an agent for its cost; it stays only as the judge of Sonnet's trials, where it is the judge already calibrated. 96 new trials; no session of work runs more than 30.


## Session 7 - `0.7.0` - Would the charter have stopped a drift that really happened?

**Shows**: a commit of REPS in which a decision moved between the model and code unnoticed, replayed with a charter and the rule, and whether the agent stops where the history did not.

Every number before this one comes from four synthetic seams of one file each. REPS is a real project with seams in cascade. The replay's tickets are written once the commit is found.

1. **Find a commit that drifted, in REPS.** Candidates from its history, one proposed - [ticket](docs/work/7-real-project/issues/01-find-the-commit.md)

## Parked

No session yet.

- Hosts other than Claude Code (version 2).
- Candidate skills: `budget`, `agent-topology`, `failure-triage`, `context-budget`.
- The author's personal `roadmap` skill, outside this repo: support for GitHub Issues, sessions against milestones.
