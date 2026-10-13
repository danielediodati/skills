# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; [openpoints.md](openpoints.md) holds what is still undecided.

A session is a milestone: it ends with something that can be shown. Its tickets are files under `docs/work/<session>-<name>/issues/`. A closed ticket is deleted and its line here is removed.

## Session 1 - `0.1.0` - Does a charter change what a coding agent does?

**Shows**: a table, per request, of where each decision ended up with and without the seam charter, judged blind to the condition.

The plugin rests on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does when it works on a stochastic seam. This session tests it on atomic seams before any further skill is written. If ticket 5 finds drift in fewer than 12 of its 36 trials without a charter, the problem is residual and the session stops there.

## Session 3 - `0.3.0` - Does the rule alone hold the line, without a charter?

**Shows**: a table of the silent drift rate with the rule alone, next to the rates with neither and with both, on the same eight requests, and the decision a rule fixed before any trial gives: a charter per seam stays mandatory or becomes optional.

Writing a charter for every seam is heavy, and no trial has run the rule in `AGENTS.md` without one. This session measures that arm before session 4 spends 144 more trials on the charter as it is. It did: the rule alone drifts in 11 of 24 trials, and the charter stays (`trials/results-rule-only.md`). A charter the agent writes alone from the code drifts in 2 of 24: the skill can draft it, and the user reviews what the code does not show (`trials/results-auto-charter.md`).

## Session 4 - `0.4.0` - How much does a charter change from one draft to the next?

**Shows**: a table of 24 charters, three per seam from Sonnet and three from Opus, each written from the code with nobody to ask, read line by line against the user's: which lines every draft finds, which none does, which depend on the draft.

Session 3 found that a charter Sonnet wrote alone from the code drifts in 2 of 24 trials, against 15 with no charter and 0 with the user's (`trials/results-auto-charter.md`). The user decided the published number is about that charter, the one the `charter` skill will ship. Session 3 had one draft per seam; this session writes the drafts the next two will use, freezes their protocol, and says what a draft can be trusted on before a trial is spent. No trial runs here.

1. **A new protocol, and three drafts per seam and model.** The protocol, the `drafted` condition, 24 charters - [ticket](docs/work/4-charter-drafts/issues/01-protocol-and-drafts.md)
2. **Read the 24 drafts against the user's charters.** Line by line - [ticket](docs/work/4-charter-drafts/issues/02-read-the-drafts.md)

## Session 5 - `0.5.0` - How much does a charter Sonnet wrote cut its silent drift?

**Shows**: a section of the README with Sonnet's silent drift rate, with no charter and with one it wrote from the code and nobody read, with its intervals, measured under the protocol session 4 froze.

Sixteen problem-only requests, three runs each, one draft per run, judged by Opus against the user's charters. 72 new trials; no session of work runs more than 30.

1. **Sonnet on requests 04 and 05, with its drafts.** 24 trials - [ticket](docs/work/5-sonnet-drift/issues/01-sonnet-04-05.md)
2. **Sonnet on requests 06.** 24 trials - [ticket](docs/work/5-sonnet-drift/issues/02-sonnet-06.md)
3. **Sonnet on requests 07.** 24 trials - [ticket](docs/work/5-sonnet-drift/issues/03-sonnet-07.md)
4. **Calibrate the judge of Sonnet's trials.** Eight trials, condition hidden - [ticket](docs/work/5-sonnet-drift/issues/04-calibration.md)
5. **Sonnet's result, and its number in the README.** As the protocol's rule gives it - [ticket](docs/work/5-sonnet-drift/issues/05-results.md)

## Session 6 - `0.6.0` - And a charter Opus wrote, its own?

**Shows**: the README section with Opus's rate beside Sonnet's, each with its intervals, never compared with each other.

The same protocol with Opus as agent and writer of its charters, judged by Sonnet. 96 new trials; no session of work runs more than 30.

1. **Opus on requests 04.** 24 trials - [ticket](docs/work/6-opus-drift/issues/01-opus-04.md)
2. **Opus on requests 05.** 24 trials - [ticket](docs/work/6-opus-drift/issues/02-opus-05.md)
3. **Opus on requests 06.** 24 trials - [ticket](docs/work/6-opus-drift/issues/03-opus-06.md)
4. **Opus on requests 07.** 24 trials - [ticket](docs/work/6-opus-drift/issues/04-opus-07.md)
5. **Calibrate the judge of Opus's trials.** Seven trials, condition hidden - [ticket](docs/work/6-opus-drift/issues/05-calibration.md)
6. **Opus's result, and its number in the README.** As the protocol's rule gives it - [ticket](docs/work/6-opus-drift/issues/06-results.md)
