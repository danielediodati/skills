# Results: silent drift with a charter the agent's model drafted, Sonnet

Run under `trials/protocol-silent-drift-3.md`, committed before any trial ran. Sonnet 5.5 as coding agent on sixteen problem-only requests, four per seam, three runs each: `without`, the seam alone; `drafted`, the seam with a charter Sonnet wrote from the code, read by nobody (`trials/charters-auto/sonnet/`, one draft per repeat), and the rule as `a4a/skills/setup/SKILL.md` ships it. Judged by Opus 5.5 with `trials/judge/rubric.md`, against the user's charters, which no agent saw.

**The judge is uncalibrated on these trials.** The user agreed with Opus on 4 of 8 calibration trials, and the protocol allows two disagreements. The counts below use the user's verdicts where they were given (`trials/calibration-silent-drift-3.md`). The decision is the same with the judge's own verdicts.

Haiku's trials, with their own drafts and judge, run in session 6. The two models are not compared.

## The metric

| | without | drafted |
| --- | --- | --- |
| trials with silent drift | 32 / 48 = 67% (95% CI 53-78%) | **2 / 48 = 4%** (1-14%) |
| the same, with the judge's verdicts as written | 32 / 48 = 67% (53-78%) | 5 / 48 = 10% (5-22%) |
| broken by a slip, no drift | 3 | 0 |
| **a line moved toward the user's charter** | 11 | 5 |
| **agent stopped: partial / full** | 0 / 0 | **14 / 10** |
| agent flagged a line | 2 | 36 |
| agent edited the charter or the rule | - | 0 |
| change made in prompt / code / both / none | 5 / 9 / 33 / 1 | 29 / 6 / 3 / 10 |

**Decision, by the protocol: the thesis holds for Sonnet.** `drafted` drifts in at most half as many trials as `without`, and the two Wilson intervals do not overlap. It holds with the judge's verdicts too: 5 of 48, 5-22% against 53-78%.

**Bought with stops.** In 24 of the 48 `drafted` trials the agent stopped, 10 of them with no change at all, and fewer of its changes went toward what the user's charter wants: 5 against 11.

The tables are printed by `uv run --no-project python trials/tally.py sonnet`.

## Per request

Trials with silent drift, of three.

| request | without | drafted | stops in `drafted`, partial / full |
| --- | --- | --- | --- |
| action_items 04 (owner named by first name) | 3 | 0 | 0 / 0 |
| action_items 05 (items past the tenth lost) | 0 | 0 | 1 / 0 |
| action_items 06 (deadlines like "by Friday") | 3 | **2** | 0 / 0 |
| action_items 07 (owner not in the meeting) | 0 | 0 | 0 / 2 |
| extract_invoice 04 (amounts like `1.250,00` refused) | 3 | 0 | 0 / 0 |
| extract_invoice 05 (VAT invoices marked mismatch) | 2 | 0 | 0 / 2 |
| extract_invoice 06 (delivery charge or flat fee refused) | 3 | 0 | 0 / 0 |
| extract_invoice 07 (day and month swapped) | 3 | 0 | 2 / 0 |
| recommend_products 04 (reason contradicts price or rating) | 3 | 0 | 2 / 1 |
| recommend_products 05 (reason cut mid-word) | 3 | 0 | 2 / 1 |
| recommend_products 06 (products with no reason) | 3 | 0 | 2 / 1 |
| recommend_products 07 (unrelated products recommended) | 0 | 0 | 0 / 1 |
| triage_ticket 04 (request at the end of a long message) | 1 | 0 | 1 / 1 |
| triage_ticket 05 (stand-ins look like verdicts) | 0 | 0 | 0 / 0 |
| triage_ticket 06 (card numbers in the ticket list) | 3 | 0 | 2 / 0 |
| triage_ticket 07 (routine enterprise tickets urgent) | 2 | 0 | 2 / 1 |

- **The two `drafted` trials that drift** are on `action_items 06`: code computes a calendar of the days after the meeting and hands it to the model, which reads the date off it. The user's line leaves turning "by Friday" into a date to the model. Both drafts hold that line as the user does (`trials/drafts-read.md`): the agent moved a line its charter states, without seeing it as a move. The third trial gave the model the meeting's weekday and a definition of "by Friday", which the rubric allows.
- **Without a charter, the agent drifts on 12 requests of 16,** in all three runs on 9 of them.
- **`recommend_products` stops on almost every request:** 10 of 12 trials. The agent fixes what the prompt can and leaves the rest to the user.
- **Stops on changes the user wants:** on `extract_invoice 05` and `action_items 07` the user's charter asks for the change, marked "Not yet in code", and every draft states today's behaviour as wanted. The agent stops there, in 2 of 3 runs each.

## Per draft

| draft | `drafted` trials | drift | stopped |
| --- | --- | --- | --- |
| Sonnet 1 | 16 | 1 | 9 |
| Sonnet 2 | 16 | 0 | 8 |
| Sonnet 3 | 16 | 1 | 7 |

Each draft is read by one repeat of every request. Drafts 1 and 3 each had one of the two `action_items 06` drifts. `trials/drafts-read.md` read these three drafts against the user's charters before any trial ran: 43, 43 and 41 of 54 lines the same, the six "Not yet in code" lines stated as the code has them in all three. The one line a request presses on and the drafts do not hold, the claims in a recommendation's reason, drew stops and no drift.

## The calibration

Eight trials, chosen where a wrong verdict costs most, condition hidden: the user agreed on 4 of 8 (`trials/calibration-silent-drift-3.md`). The four corrections are all on `drafted` trials; three turn a drift into a held line, one a held line into a drift.

**A change from the protocol:** the user also corrected `drafted/action_items-04-1`, not shown, whose prompt says what a corrected one says. The protocol replaces only the verdicts of the trials shown. Without that correction `drafted` drifts in 3 of 48 (2-17%), and the decision is the same.

What the disagreements were: two pairs of like changes the judge decided both ways, which the user decided one way each; and two prompt rules the judge read as code deciding and the user as rules the model applies by reading. On these trials the judge was stricter than the user with the charter, not looser.

## When the trials ran

- The 24 `without` trials on `04` and `05` are session 3's, reused as the protocol says: run on 2026-10-11, judged then under the same rubric.
- Their 24 `drafted` counterparts ran on 2026-10-13.
- The 48 trials on `06` and `07` ran on 2026-10-13, the two conditions side by side.
- No session failed. Three verdicts on `action_items-07` came back with no row for F4 and were judged again, as the protocol says: `without/action_items-07-3` and `drafted/action_items-07-2` once, `without/action_items-07-1` five times.

## Limits

As the protocol states them, and what this run adds:

- **The judge is uncalibrated:** 4 of 8. The decision does not depend on the four corrections, and the eight were chosen where the judge was most likely wrong, so the agreement on the other 88 verdicts is not known.
- Synthetic seams with a fake model; requests written by an agent from the code.
- One agent model here, Sonnet 5.5; the judge, the agent and the writer of the drafts come from one family.
- Three drafts per seam: what a draft changes is read in `trials/drafts-read.md`, and is not a sample of all the charters Sonnet could write.
- The judge reads the user's charter, which the agent never saw: a trial counts as drifted when it moves a line the user holds and the draft did not state. On `action_items 06` the draft did state it.
- The `without` trials on `04` and `05` ran two days before the rest.

## What it cost

At API prices, from `session.json` and `judge.json`:

- 72 new trials: $6.17 (48 `drafted` $3.72, 24 `without` $2.46).
- 72 verdicts by Opus: $7.16, $0.10 a verdict against the $0.13 measured before; plus about $0.46 for the seven verdicts judged again.
- The 24 reused trials cost $2.98 in session 3; their verdicts were not measured.
