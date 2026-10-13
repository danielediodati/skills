# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; [openpoints.md](openpoints.md) holds what is still undecided.

A session is a milestone: it ends with something that can be shown. Its tickets are files under `docs/work/<session>-<name>/issues/`. A closed ticket is deleted and its line here is removed.

## Session 1 - `0.1.0` - Does a charter change what a coding agent does?

**Shows**: a table, per request, of where each decision ended up with and without the seam charter, judged blind to the condition.

The plugin rests on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does when it works on a stochastic seam. This session tests it on atomic seams before any further skill is written. If ticket 5 finds drift in fewer than 12 of its 36 trials without a charter, the problem is residual and the session stops there.

## Session 5 - `0.5.0` - How much does a charter Sonnet wrote cut its silent drift?

**Shows**: a section of the README with Sonnet's silent drift rate, with no charter and with one it wrote from the code and nobody read, with its intervals, measured under the protocol session 4 froze.

Sixteen problem-only requests, three runs each, one draft per run, judged by Opus against the user's charters. 72 new trials; no session of work runs more than 30.

3. **Sonnet on requests 07.** 24 trials - [ticket](docs/work/5-sonnet-drift/issues/03-sonnet-07.md)
4. **Calibrate the judge of Sonnet's trials.** Eight trials, condition hidden - [ticket](docs/work/5-sonnet-drift/issues/04-calibration.md)
5. **Sonnet's result, and its number in the README.** As the protocol's rule gives it - [ticket](docs/work/5-sonnet-drift/issues/05-results.md)

## Session 6 - `0.6.0` - And a charter Haiku wrote, its own?

**Shows**: the README section with Haiku's rate beside Sonnet's, each with its intervals, never compared with each other.

The same protocol with Haiku as agent and writer of its charters, judged by Sonnet. Haiku, not Opus: the user set Opus aside as an agent for its cost; it stays only as the judge of Sonnet's trials, where it is the judge already calibrated. 96 new trials; no session of work runs more than 30.

1. **Haiku on requests 04.** 24 trials - [ticket](docs/work/6-haiku-drift/issues/01-haiku-04.md)
2. **Haiku on requests 05.** 24 trials - [ticket](docs/work/6-haiku-drift/issues/02-haiku-05.md)
3. **Haiku on requests 06.** 24 trials - [ticket](docs/work/6-haiku-drift/issues/03-haiku-06.md)
4. **Haiku on requests 07.** 24 trials - [ticket](docs/work/6-haiku-drift/issues/04-haiku-07.md)
5. **Calibrate the judge of Haiku's trials.** Seven trials, condition hidden - [ticket](docs/work/6-haiku-drift/issues/05-calibration.md)
6. **Haiku's result, and its number in the README.** As the protocol's rule gives it - [ticket](docs/work/6-haiku-drift/issues/06-results.md)

## Session 7 - `0.7.0` - Would the charter have stopped a drift that really happened?

**Shows**: a commit of REPS in which a decision moved between the model and code unnoticed, replayed with a charter and the rule, and whether the agent stops where the history did not.

Every number before this one comes from four synthetic seams of one file each. REPS is a real project with seams in cascade. The replay's tickets are written once the commit is found.

1. **Find a commit that drifted, in REPS.** Candidates from its history, one proposed - [ticket](docs/work/7-real-project/issues/01-find-the-commit.md)

## Parked

No session yet.

- Hosts other than Claude Code (version 2).
- Candidate skills: `budget`, `agent-topology`, `failure-triage`, `context-budget`.
- The author's personal `roadmap` skill, outside this repo: support for GitHub Issues, sessions against milestones.
