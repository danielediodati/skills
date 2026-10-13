# Roadmap

The order things get built in. [CONTEXT.md](CONTEXT.md) holds the vocabulary and the decisions; [openpoints.md](openpoints.md) holds what is still undecided.

A session is a milestone: it ends with something that can be shown. Its tickets are files under `docs/work/<session>-<name>/issues/`. A closed ticket is deleted and its line here is removed.

## Session 1 - `0.1.0` - Does a charter change what a coding agent does?

**Shows**: a table, per request, of where each decision ended up with and without the seam charter, judged blind to the condition.

The plugin rests on one untested claim: a seam charter plus the rule in `AGENTS.md` changes what a coding agent does when it works on a stochastic seam. This session tests it on atomic seams before any further skill is written. If ticket 5 finds drift in fewer than 12 of its 36 trials without a charter, the problem is residual and the session stops there.

## Session 3 - `0.3.0` - Does the rule alone hold the line, without a charter?

**Shows**: a table of the silent drift rate with the rule alone, next to the rates with neither and with both, on the same eight requests, and the decision a rule fixed before any trial gives: a charter per seam stays mandatory or becomes optional.

Writing a charter for every seam is heavy, and no trial has run the rule in `AGENTS.md` without one. This session measures that arm before session 4 spends 144 more trials on the charter as it is.

1. **The rule alone, without a charter.** A protocol, 24 trials, the decision - [ticket](docs/work/3-rule-only/issues/01-rule-only.md)

## Session 4 - `0.4.0` - How much does the charter cut silent drift, with Sonnet and Opus?

**Shows**: a section of the README with the silent drift rate per agent model, with and without the charter, with its intervals, measured under a protocol fixed before any trial ran.

Session 1's first trials mostly dictated the fix; on eight requests that only describe a problem, Sonnet drifted in 14 of 24 trials without the charter and 2 of 24 with it (`trials/results-silent-drift.md`). This session makes that a number worth publishing: sixteen problem-only requests, Sonnet and Opus, each model's trials judged by the other, under `trials/protocol-silent-drift-2.md`. No session of work runs more than 30 trials.

3. **Judge the reused Sonnet trials again.** The 48 trials on requests 04 and 05, with the frozen rubric - [ticket](docs/work/4-silent-drift/issues/03-rejudge-reused.md)
4. **Sonnet on requests 06.** 24 trials - [ticket](docs/work/4-silent-drift/issues/04-sonnet-06.md)
5. **Sonnet on requests 07.** 24 trials - [ticket](docs/work/4-silent-drift/issues/05-sonnet-07.md)
6. **Opus on requests 04.** 24 trials - [ticket](docs/work/4-silent-drift/issues/06-opus-04.md)
7. **Opus on requests 05.** 24 trials - [ticket](docs/work/4-silent-drift/issues/07-opus-05.md)
8. **Opus on requests 06.** 24 trials - [ticket](docs/work/4-silent-drift/issues/08-opus-06.md)
9. **Opus on requests 07.** 24 trials - [ticket](docs/work/4-silent-drift/issues/09-opus-07.md)
10. **Calibrate the two judges.** Fifteen trials, condition and model hidden - [ticket](docs/work/4-silent-drift/issues/10-calibration.md)
11. **The result, and the number in the README.** Per model, as the protocol's rule gives it - [ticket](docs/work/4-silent-drift/issues/11-results.md)
