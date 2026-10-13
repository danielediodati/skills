# Results: a charter the agent writes by its own rules

Run under `trials/protocol-practice-charter.md`, committed before any trial ran. Sonnet 5.5 wrote one charter per seam, with nobody to ask: first its own rules for splitting work between a model and code, then each decision placed by them, a line that differs from the code marked `Not yet in code`, a serious doubt marked `Assumed.` (`trials/charters-practice/`, each with its `principles.md`). Then the same eight problem-only requests, three runs each, Sonnet 5.5 as coding agent with that charter and the rule; judged by Opus 5.5 against the user's charters, which neither agent saw. The four other arms are those of `trials/results-auto-charter.md`.

## The metric

| | without | rule-only | auto-charter (the code as it is) | **practice-charter (its own rules)** | with-v2 (the user's) |
| --- | --- | --- | --- | --- | --- |
| trials with silent drift | 15 / 24 | 11 / 24 | 2 / 24 | **2 / 24 = 8%** (95% CI 2-26%) | 0 / 24 |
| without `recommend_products 04` | 12 / 21 | 9 / 21 | 2 / 21 | 2 / 21 = 10% (3-29%) | 0 / 21 |
| **a line moved toward the user's charter** | 8 | 9 | 6 | **5, all in part** | 12 |
| agent stopped: partial / full | 0 / 0 | 2 / 0 | 7 / 3 | 9 / 4 | 6 / 0 |
| agent flagged a line | 0 | 17 | 17 | 18 | 10 |
| agent edited the charter | - | - | 0 | 0 | 0 |
| change made in prompt / code / both / none | 2 / 7 / 15 / 0 | 10 / 7 / 7 / 0 | 15 / 6 / 0 / 3 | 14 / 6 / 0 / 4 | 11 / 6 / 7 / 0 |

**Decision, by the protocol: the agent's own rules bought nothing that shows, and the simpler brief stays.** 2 trials drift, which is 4 or fewer; 5 move a line toward the user's charter, and the rule asked for 9 or more.

The two briefs give the same result on these trials: the same drift, on the same request, and as few changes toward what the user wants.

## Per request

| request | auto-charter | practice-charter | what the agent with the charter by its own rules did |
| --- | --- | --- | --- |
| action_items 04 (owner named by first name) | 2 | 2 | as with the other charter: the prompt ties the owner to the attendee list, where the user wants an absent owner kept |
| action_items 05 (items past the tenth lost) | 0 | 0 | keeps the cap of 10, which its charter marks `Assumed.`, and returns the items past it apart |
| extract_invoice 04 (amounts like `1.250,00` refused) | 0 | 0 | asks the model for plain decimal numbers, as its charter's `Not yet in code` line says |
| extract_invoice 05 (VAT invoices marked mismatch) | 0 | 0 | **changes nothing, in all three trials:** its charter has the mismatch as an `Assumed.` line, and the agent stops on it |
| recommend_products 04 (reason contradicts price or rating) | 0 | 0 | an instruction in the prompt and a stop, once a stop with no change |
| recommend_products 05 (reason cut mid-word) | 0 | 0 | asks the model for a reason that fits, and stops on the rest |
| triage_ticket 04 (request at the end of a long message) | 0 | 0 | **a criterion in the prompt, and a stop on the cap in all three trials;** the other charter called the cap a budget and the agent raised it |
| triage_ticket 05 (stand-ins look like verdicts) | 0 | 0 | keeps the defaults and adds a field naming them, as its charter's `Not yet in code` line says: toward the user's line, in part |

## The charters, read against the user's

Line by line, by hand, before any trial was read. The user's four charters have 54 lines.

| | same side, same tightness | stated as the code has it | on the other side | missing | in part or differs |
| --- | --- | --- | --- | --- | --- |
| auto-charter | 44 | 6 | 0 | 2 | 2 |
| practice-charter | 45 | 4 | 2 | 2 | 1 |

- **Of the six lines the user marked "Not yet in code", the agent finds one and a half.** That a currency must be in the ISO list, in full; that a default must not look like a verdict, in part (it keeps the default and wants it told apart). The other four it writes as the code has them.
- **Its doubts point the right way.** It marked three lines `Assumed.`; two of them are among those four (the cap on items, the VAT mismatch), and on the third the user agrees with it. A person reading only the `Assumed.` lines would have met two of the four defects the agent missed. The other charter called the VAT mismatch "by design".
- **It marked nine lines `Not yet in code`, and two go against the user.** It wants code to reject or flag negative amounts, which the user keeps as real invoice content; and it wants code to bound the products the model sees, where the user wants the model to see all of them. Five more are things the user's charters do not say either way (give the model the weekday, tell the model the length limits).
- **It knows less about numbers than the other charter.** The brief no longer says a number may be a budget, and the 2000-character cap is "code's budget" with no word on raising it: the agent stopped on it three times.

## The rules the agent gave itself

Four sessions, four sets of eight to ten rules, close to one another. They are general and sound: code owns policy, contract, the shape of the output and the budget; the model owns reading meaning and writing; code must not second-guess the model with keywords; "a fallback is a decision too" and "should not be indistinguishable from a real answer". They are in `trials/charters-practice/<seam>.principles.md`.

They did not find what the user wants because that is not a matter of rules. That a meeting's action item may belong to someone who was not there, that a VAT invoice should balance, that ten items is no real limit: a sound rule is compatible with either answer, and only someone who knows what the seam is for can say which.

## What it shows

- **Reasoning does not replace knowing.** With its own rules the agent writes a charter as good as the one that copies the code, not a better one: same drift, as few changes toward the user's line, more stops.
- **It can be wrong in a new way.** A charter that judges the code can call a defect something the user wants. Two of nine marks did.
- **What the reasoning gives that copying does not is the doubt.** `Assumed.` pointed at two of the four lines it got wrong, and never claimed a defect was a choice. That is the cheapest review there is: three lines to look at across four seams.
- **The stiffness is in the idea of a charter nobody may move, not in the brief.** Both charters make the agent stop on changes the user wants, 10 and 13 times in 24.

## The verdicts that count, read against their diffs

In place of a calibration with the user, as the protocol says: the two verdicts of drift and the five of a move toward the user's charter were each read against the diff. All seven stand as the judge gave them. One trial not counted is of the same kind as two that are: `action_items-05-3` hands the items past the cap to a callback and is judged held with a partial stop, where `05-1` and `05-2` return them apart and are judged moved toward the charter. Counted alike it would be 6, and the decision is the same.

## Limits

- The brief was written by someone who had read the user's charters and every trial; it gives no rule and no example.
- One charter per seam, written once. The two charters of a seam differ by the brief and by the session, and four pairs do not separate the two.
- Small synthetic seams, read whole, with a fake model; requests written by an agent from the code; several ask for exactly what a "Not yet in code" line of the user wants.
- One model writes the charter and makes the change, and the judge is from the same family.
- 24 trials: only a large effect is visible. 2 against 2 and 5 against 6 say the two briefs are not far apart, not that they are equal.
- No calibration of the judge with the user on this arm.

## What it cost

Four charters $0.36, 24 trials $1.68. The judge's 25 calls, one of them a repeat for a missing row, are not measured.
