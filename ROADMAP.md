# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; [openpoints.md](openpoints.md) holds what is still undecided.

A session is a milestone: it ends with something that can be shown. Its tickets are files under `docs/work/<session>-<name>/issues/`. A closed ticket is deleted and its line here is removed.

## Session 1 - `0.1.0` - Does a charter change what a coding agent does?

**Shows**: a table, per request, of where each decision ended up with and without the seam charter, judged blind to the condition.

The plugin rests on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does when it works on a stochastic seam. This session tests it on atomic seams before any further skill is written. If ticket 5 finds drift in fewer than 12 of its 36 trials without a charter, the problem is residual and the session stops there.

7. **Close the back door in the rule.** A rule that forbids the agent to edit the charter, and the trials with the charter run again - [ticket](docs/work/1-charter-trial/issues/07-rule-v2.md)
