# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; [openpoints.md](openpoints.md) holds what is still undecided.

A session is a milestone: it ends with something that can be shown. Its tickets are files under `docs/work/<session>-<name>/issues/`. A closed ticket is deleted and its line here is removed.

## Session 1 - `0.1.0` - Does a charter change what a coding agent does?

**Shows**: a table, per request, of where each decision ended up with and without the seam charter, judged blind to the condition.

The plugin rests on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does when it works on a stochastic seam. This session tests it on atomic seams before any further skill is written. If ticket 5 finds drift in fewer than 12 of its 36 trials without a charter, the problem is residual and the session stops there.

## Session 3 - `0.3.0` - Does the rule alone hold the line, without a charter?

**Shows**: a table of the silent drift rate with the rule alone, next to the rates with neither and with both, on the same eight requests, and the decision a rule fixed before any trial gives: a charter per seam stays mandatory or becomes optional.

Writing a charter for every seam is heavy, and no trial has run the rule in `AGENTS.md` without one. This session measures that arm before session 4 spends 144 more trials on the charter as it is. It did: the rule alone drifts in 11 of 24 trials, and the charter stays (`trials/results-rule-only.md`). A charter the agent writes alone from the code drifts in 2 of 24: the skill can draft it, and the user reviews what the code does not show (`trials/results-auto-charter.md`).

## Session 4 - `0.4.0` - How much does a charter the agent wrote cut silent drift, with Sonnet and Opus?

**Shows**: a section of the README with the silent drift rate per agent model, with no charter and with one the same model wrote from the code and nobody read, with its intervals, measured under a protocol fixed before any trial ran.

Session 3 found that a charter Sonnet wrote alone from the code drifts in 2 of 24 trials, against 15 with no charter and 0 with the user's (`trials/results-auto-charter.md`). The user decided the published number is about that charter, the one the `charter` skill will ship, and not about the one written with the user. This session makes it a number worth publishing: sixteen problem-only requests, Sonnet and Opus, each model writing its own charters, three drafts per seam so the number carries how much a draft varies, each model's trials judged by the other against the user's charters. 168 new trials; no session of work runs more than 30.

3. **A new protocol, and three drafts per seam and model.** The protocol, the `drafted` condition, 24 charters - [ticket](docs/work/4-silent-drift/issues/03-protocol-and-drafts.md)
4. **Read the 24 drafts against the user's charters.** Line by line, before any trial is read - [ticket](docs/work/4-silent-drift/issues/04-read-the-drafts.md)
5. **Sonnet on requests 04 and 05, with its drafts.** 24 trials - [ticket](docs/work/4-silent-drift/issues/05-sonnet-04-05.md)
6. **Sonnet on requests 06.** 24 trials - [ticket](docs/work/4-silent-drift/issues/06-sonnet-06.md)
7. **Sonnet on requests 07.** 24 trials - [ticket](docs/work/4-silent-drift/issues/07-sonnet-07.md)
8. **Opus on requests 04.** 24 trials - [ticket](docs/work/4-silent-drift/issues/08-opus-04.md)
9. **Opus on requests 05.** 24 trials - [ticket](docs/work/4-silent-drift/issues/09-opus-05.md)
10. **Opus on requests 06.** 24 trials - [ticket](docs/work/4-silent-drift/issues/10-opus-06.md)
11. **Opus on requests 07.** 24 trials - [ticket](docs/work/4-silent-drift/issues/11-opus-07.md)
12. **Calibrate the two judges.** Fifteen trials, condition and model hidden - [ticket](docs/work/4-silent-drift/issues/12-calibration.md)
13. **The result, and the number in the README.** Per model, as the protocol's rule gives it - [ticket](docs/work/4-silent-drift/issues/13-results.md)
