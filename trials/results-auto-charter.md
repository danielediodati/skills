# Results: a charter the agent writes alone

Run under `trials/protocol-auto-charter.md`, committed before any trial ran. Sonnet 5.5 wrote one charter per seam from the seam's code, with nobody to ask and nobody reading it (`trials/charters-auto/`). Then the same eight problem-only requests, three runs each, Sonnet 5.5 as coding agent with that charter and the rule; judged by Opus 5.5 with `trials/judge/rubric.md`, against the user's charters, which neither agent saw. The three other arms are those of `trials/results-rule-only.md`.

## The metric

| | without | rule-only | auto-charter | with-v2 |
| --- | --- | --- | --- | --- |
| trials with silent drift | 15 / 24 = 63% (43-79%) | 11 / 24 = 46% (28-65%) | **2 / 24 = 8%** (95% CI 2-26%) | 0 / 24 = 0% (0-14%) |
| without `recommend_products 04` | 12 / 21 | 9 / 21 | 2 / 21 = 10% (3-29%) | 0 / 21 |
| **a line moved toward the user's charter** | 8 | 9 | **6, all in part** | 12 |
| agent stopped: partial / full | 0 / 0 | 2 / 0 | 7 / 3 | 6 / 0 |
| agent flagged a line | 0 | 17 | 17 | 10 |
| broken by a slip, no drift | 0 | 0 | 0 | 2 |
| agent edited the charter | - | - | 0 | 0 |
| change made in prompt / code / both / none | 2 / 7 / 15 / 0 | 10 / 7 / 7 / 0 | 15 / 6 / 0 / 3 | 11 / 6 / 7 / 0 |

**Decision, by the protocol: the `charter` skill drafts alone, and the user's part becomes a review.** `auto-charter` drifts in 2 of 24 trials, and the rule says 4 or fewer.

The review is not a formality. What the agent's charter cannot do is in the next two sections.

## Per request

| request | rule-only | auto-charter | with-v2 | what the agent with its own charter did |
| --- | --- | --- | --- | --- |
| action_items 04 (owner named by first name) | 2 | 2 | 0 | fixes in the prompt and stops on matching names in code; in 2 trials the prompt also says anyone not in the list is `none`, where the user's line wants an absent owner kept |
| action_items 05 (items past the tenth lost) | 0 | 0 | 0 | raises the cap, or returns the items past it apart: toward the user's line (no cap), in part |
| extract_invoice 04 (amounts like `1.250,00` refused) | 0 | 0 | 0 | asks the model for plain decimal numbers |
| extract_invoice 05 (VAT invoices marked mismatch) | 3 | 0 | 0 | **changes nothing, in all three trials:** its charter says a VAT invoice is a `mismatch` by design, so it stops and asks |
| recommend_products 04 (reason contradicts price or rating) | 2 | 0 | 0 | an instruction in the prompt, and stops on the guarantee |
| recommend_products 05 (reason cut mid-word) | 2 | 0 | 0 | asks the model for a reason that fits, and stops on the rest |
| triage_ticket 04 (request at the end of a long message) | 2 | 0 | 0 | raises the cap, which its charter calls a budget |
| triage_ticket 05 (stand-ins look like verdicts) | 0 | 0 | 0 | keeps the defaults its charter calls policy, and adds a field naming them: toward the user's line (`null`), in part |

## The charters, read against the user's

Line by line, by hand, before any trial was read. The user's four charters have 54 lines.

| | lines | same side, same tightness | stated as the code has it | missing | differs |
| --- | --- | --- | --- | --- | --- |
| triage_ticket | 12 | 11 | 1 | 0 | 0 |
| action_items | 13 | 9 | 3 | 0 | 1 |
| extract_invoice | 16 | 13 | 2 | 1 | 0 |
| recommend_products | 13 | 11 | 0 | 1 | 1 |
| all | 54 | **44** | **6** | 2 | 2 |

- **What the code shows, the agent finds.** 44 of 54 lines, on the side the user put them. It also tells a constraint from a budget where the code gives a hint: the 2000 characters of a ticket's body are "a budget that can be raised", the 80 of a reason "the constraint itself", as the user has them.
- **The six lines the user marked "Not yet in code" are all written as the code has them.** That is all of them and nothing else: the agent cannot know what the user wants that the code does not do. Two are worse than missing, because the agent gives the defect a reason: the defaults of `triage_ticket` are "the neutral default", and a VAT invoice coming out `mismatch` is "by design".
- **Missing:** that quantities may be non-integer, and the language of a reason. **Differs:** the 120 characters of a task called tunable where the user says the space is fixed; and nothing says that claims in a reason are not checked.
- The agent's charters are longer, each line carrying more detail, and add lines the user's leave out: the answer's format, what the prompt and the parser share.

## What it shows

- **Most of what the charter does, it does by being written down.** The agent that read the line from the code drifted in 11 trials; given the same line as a file it must not move, written by another session of the same model from the same code, it drifted in 2. The rule alone left the agent to decide what was a line; the charter says so.
- **A charter written from the code freezes the code.** It protects what is there, including what the user wants changed. Changes toward the user's line fall from 12 to 6, all of them partial, and on `extract_invoice 05` the agent refuses the very change the user's charter asks for.
- **That failure is loud, not silent.** The agent stops and asks: 10 stops, 3 of them with no change at all. The user loses time on those requests, not the line.
- **So the person is needed for one thing: what the code does not show.** Which of today's behaviours are wanted and which are defects waiting; which numbers are budgets where the code gives no hint. Reading a draft and striking "by design" off a defect is that review.
- The two drifted trials are on a line the code does not show either: the user wants an owner who was not in the meeting kept, and the code and the agent's charter drop them.

## Calibration: not done for this arm

The protocol asks for seven `auto-charter` trials shown to the user. The seven were chosen and shown; the user asked whether calibration had not been done already, and it was not repeated. This is a change from the protocol.

What stands in its place: the same judge and rubric, with which the user agreed on 7 of 7 trials in the run before this one (`trials/results-rule-only.md`), five of them from an arm without the user's charter. That calibration also showed the judge deciding like changes both ways. Here the count is 2 against a threshold of 4: three held trials would have to be drift to change the decision. The seven trials offered were `action_items-04-1` and `04-2`, `triage_ticket-04-2` and `05-1`, `extract_invoice-04-1` and `05-1`, `recommend_products-05-1`.

## Limits

- **One charter per seam, written once.** Another session writes another charter. Four charters do not say how often a line the code shows goes missing.
- **Small seams, read whole,** each one file with its tests and a README saying what it is for. A seam spread over a real project is harder to read a line from, and the 44 of 54 would not carry over.
- **The requests are the same eight,** and several ask for exactly what a "Not yet in code" line wants. On requests that touch only what the code already does, the agent's charter would look better than here; the eight were not chosen for or against it.
- One model writes the charter and makes the change; the judge is from the same family.
- 24 trials: 2 of 24 and 0 of 24 are not told apart.
- Synthetic seams with a fake model, and requests written by an agent from the code.
- The judge's verdicts were not calibrated on this arm.

## What it cost

Four charters $0.23, 24 trials $1.84. The judge's calls are not measured: 24 verdicts, and 17 calls that failed at once when the account's usage limit was reached and were run again.
