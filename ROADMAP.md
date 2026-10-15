# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; [openpoints.md](openpoints.md) holds what is still undecided.

A session is a milestone: it ends with something that can be shown. Its tickets are files under `docs/work/<session>-<name>/issues/`. A closed ticket is deleted and its line here is removed.

## Session 7 - `0.7.0` - Would the charter have stopped a drift that really happened?

**Shows**: a commit of REPS in which a decision moved between the model and code unnoticed, replayed with a charter and the rule, and whether the agent stops where the history did not.

Every number before this one comes from four synthetic seams of one file each. REPS is a real project with seams in cascade. The replay's tickets are written once the commit is found.

1. **Find a commit that drifted, in REPS.** Candidates from its history, one proposed - [ticket](docs/work/7-real-project/issues/01-find-the-commit.md)

## Session 8 - `0.8.0` - The repository public

**Shows**: the repository public on GitHub, with a README that teaches the plugin through one example and states what the numbers do and do not show.

1. **Session 7 on its own branch.** `main` without the unrun replay - [ticket](docs/work/8-public-repo/issues/01-session-7-on-a-branch.md)
2. **The tree cleaned.** Nothing of the author's machine - [ticket](docs/work/8-public-repo/issues/02-the-tree-cleaned.md)
3. **The history cleaned.** One rewrite before anything is public - [ticket](docs/work/8-public-repo/issues/03-the-history-cleaned.md)
4. **The README.** The problem, the plugin, one example, the numbers - [ticket](docs/work/8-public-repo/issues/04-the-readme.md)
5. **Public.** Pushed, checked, made public by the user - [ticket](docs/work/8-public-repo/issues/05-public.md)

## Parked

No session yet.

- Hosts other than Claude Code (version 2).
- Candidate skills: `budget`, `agent-topology`, `failure-triage`, `context-budget`.
- The author's personal `roadmap` skill, outside this repo: support for GitHub Issues, sessions against milestones.
