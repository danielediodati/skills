# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; [openpoints.md](openpoints.md) holds what is still undecided.

A session is a milestone: it ends with something that can be shown. Its tickets are files under `docs/work/<session>-<name>/issues/`. A closed ticket is deleted and its line here is removed.

## Session 1 - `0.1.0` - Does a charter change what a coding agent does?

**Shows**: a table, per request, of where each decision ended up with and without the seam charter, judged blind to the condition.

The plugin rests on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does when it works on a stochastic seam. This session tests it on atomic seams before any further skill is written. If ticket 5 finds drift in fewer than 12 of its 36 trials without a charter, the problem is residual and the session stops there.

2. **Four atomic seams and their requests.** Written by an agent that has read only the brief - [ticket](docs/work/1-charter-trial/issues/02-seams-and-requests.md)
3. **One charter per seam.** Written by the user with the `charter` skill, before reading the requests - [ticket](docs/work/1-charter-trial/issues/03-charters.md)
4. **The judging rubric.** What a judge is asked about a change, blind to the condition - [ticket](docs/work/1-charter-trial/issues/04-rubric.md)
5. **Is there drift?** Every request given to a coding agent without the charter, and the judge calibrated on the user's labels - [ticket](docs/work/1-charter-trial/issues/05-drift-without-charter.md)
6. **Does the charter reduce it?** Every request, given again with the charter and the rule - [ticket](docs/work/1-charter-trial/issues/06-drift-with-charter.md)
