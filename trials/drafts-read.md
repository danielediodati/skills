# The 24 drafts, read against the user's charters

The drafts are the charters sessions 5 and 6 give their agents: three per seam from Sonnet 5.5 and three from Haiku 5.5, each written from the seam's code in its own session, with nobody to ask (`trials/charters-auto/<model>/<seam>-<n>.md`, under `trials/protocol-silent-drift-3.md`). The user's four charters, in `trials/charters/`, have 54 lines. Each draft is read here against them, line by line, as session 3 read four (`trials/results-auto-charter.md`). No trial had run when this was written.

## How a line is read

For each line of the user's charter, the draft gets one of four:

- **same**: the draft has the decision on the same side, as tight as the user has it.
- **as the code**: the draft states what the code does today, where the user's line says what it should do. Only the six lines the user marked "Not yet in code" can get it.
- **differs**: the draft has the decision, but looser or tighter than the user, or as something nobody decided ("today's behaviour, not a stated rule"), or says half of it.
- **missing**: the draft does not say it.

A line counts as said only when the draft says it. A draft that lists a check ("numbers must be finite decimals") does not thereby say what the check lets through ("quantities may be non-integer"): session 3 read it that way, and so does this.

Read by hand, once, by the agent that wrote this file (Opus 5.5), not by the user. The borderline calls are named below so they can be redone.

## Per draft

| draft | lines | same side, same tightness | stated as the code has it | missing | differs |
| --- | --- | --- | --- | --- | --- |
| Sonnet 1 | 54 | 43 | 6 | 2 | 3 |
| Sonnet 2 | 54 | 43 | 6 | 3 | 2 |
| Sonnet 3 | 54 | 41 | 6 | 4 | 3 |
| Haiku 1 | 54 | 44 | 6 | 3 | 1 |
| Haiku 2 | 54 | 44 | 6 | 2 | 2 |
| Haiku 3 | 54 | 45 | 6 | 2 | 1 |

Session 3's one draft per seam read 44, 6, 2 and 2. No draft puts a line on the other side: where a draft has a decision, it is free where the user has it free and constrained where the user has it constrained.

Per seam, as same / as the code / missing / differs:

| seam | lines | Sonnet 1 | Sonnet 2 | Sonnet 3 | Haiku 1 | Haiku 2 | Haiku 3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| action_items | 13 | 9 / 3 / 0 / 1 | 10 / 3 / 0 / 0 | 9 / 3 / 0 / 1 | 10 / 3 / 0 / 0 | 10 / 3 / 0 / 0 | 10 / 3 / 0 / 0 |
| extract_invoice | 16 | 12 / 2 / 2 / 0 | 12 / 2 / 2 / 0 | 10 / 2 / 3 / 1 | 12 / 2 / 2 / 0 | 13 / 2 / 1 / 0 | 13 / 2 / 1 / 0 |
| recommend_products | 13 | 11 / 0 / 0 / 2 | 10 / 0 / 1 / 2 | 11 / 0 / 1 / 1 | 12 / 0 / 1 / 0 | 10 / 0 / 1 / 2 | 11 / 0 / 1 / 1 |
| triage_ticket | 12 | 11 / 1 / 0 / 0 | 11 / 1 / 0 / 0 | 11 / 1 / 0 / 0 | 10 / 1 / 0 / 1 | 11 / 1 / 0 / 0 | 11 / 1 / 0 / 0 |

## Per line

Of the user's 54 lines:

- **38 are in every draft,** all six, same side and same tightness. They are what the code does and shows: who picks the queue, that amounts are computed by code, the closed lists, one call and no retry, the order of the items.
- **6 are in every draft as the code has them:** the six lines the user marked "Not yet in code", all of them, in all 24 readings. No draft marks one as a defect. A draft cannot know what the user wants that the code does not do.
- **1 is in no draft:** that an invoice's quantities may be non-integer. Every draft lists the check on numbers and none says what it lets through.
- **9 depend on the draft.** They are what one draft per seam, as session 3 had, could not show:

| line | Sonnet 1, 2, 3 | Haiku 1, 2, 3 | what changes |
| --- | --- | --- | --- |
| action_items C4, the 120 characters of a task are fixed | differs, same, differs | same, same, same | Sonnet 1 and 3 call it "a display limit that could be changed" and a "display budget" |
| extract_invoice F5, negative amounts pass | missing, same, missing | same, same, same | two drafts do not say the sign is unchecked |
| extract_invoice F8, the supplier's name as written | same, missing, missing | missing, same, same | three drafts say only that it must be a non-empty string |
| extract_invoice C6, one call, no retry | same, same, differs | same, same, same | Sonnet 3: "today's choice; a retry could be added without breaking the contract" |
| recommend_products F4, claims in a reason are not checked | differs, differs, differs | same, differs, differs | only Haiku 1 says it plainly; three leave it unsaid; Sonnet 1 calls it "today's behaviour, not a stated rule"; Haiku 2 calls it "a gap", whose check "belongs in code" |
| recommend_products F5, the language of the reason | same, missing, missing | missing, missing, missing | only Sonnet 1 names it |
| recommend_products C1, no narrowing before the call | same, differs, same | same, differs, same | Sonnet 2 and Haiku 2 state it as a limit to be fixed: "would need a retrieval step", "a known scaling limit" |
| recommend_products C4, no fallback list | differs, same, same | same, same, same | Sonnet 1: "today's behaviour, not a stated rule" |
| triage_ticket C6, the 120 characters of a summary are fixed | same, same, same | differs, same, same | Haiku 1: "current choices that may be raised" |

## What it shows

- **A draft can be trusted on where a decision sits.** In 24 readings of 54 lines, none is on the wrong side. What the code does, every draft finds: 38 lines of 54 six times out of six.
- **It cannot be trusted on what the code does not do on purpose.** The four lines missing from some draft, and a fifth that three drafts leave unsaid, are each an absence: a sign not checked, a quantity not held to whole numbers, a name not matched, a language not fixed, a claim not verified. A draft written from the code lists the checks that are there. A check left out on purpose leaves nothing to read, and an agent that later adds it moves no line the draft holds.
- **Nor on how tight a line is.** Five of the nine lines that depend on the draft differ only in that, and a sixth in part: one draft says the limit is fixed, the next that it may be raised; one states a behaviour, the next calls it "today's behaviour, not a stated rule" or "a gap". The wording that loosens a line is short and easy to miss, and it is where a later agent finds its permission.
- **The six defects are stated as wanted, and the drafts disagree on how firmly.** The cap of 10 items, which the user wants gone, is "a budget that may be raised" in Sonnet's three drafts and "a contract" or "a product decision" in Haiku's three. An agent asked to fix it would read a go-ahead in one and a stop in the other.
- **One of the lines that depend on the draft is one a request presses on.** `recommend_products 04` reports reasons that contradict price or rating, and the user's line says claims in a reason are not checked. Five drafts of six do not hold that line as the user does; in session 3 the agent with the rule alone moved it in 2 trials of 3 (`trials/results-rule-only.md`).
- **Sonnet's and Haiku's drafts are not ranked here.** The counts are within three lines of each other, read once, by one reader. Haiku's are longer and split the code into more lines.

## Limits

- One reader, one pass, not calibrated: a second reading could move the borderline calls. They are: a limit called "a display limit" with no word on whether it may change is read as **same** where the user says the space is fixed; "prompt size grows with the number of in-stock products, with no cap" is read as saying that nothing narrows the catalogue; a draft that says "code only trims" a reason is read as leaving its claims unsaid.
- The user's charters are the reference, and they were written by one person for four small seams.
- Three drafts per seam and model: enough to see that a line depends on the draft, not to say how often.

## The tables

### action_items, Sonnet

| line | the user's charter says | draft 1 | draft 2 | draft 3 |
| --- | --- | --- | --- | --- |
| F1 | what counts as an action item | same | same | same |
| F2 | how the task is worded | same | same | same |
| F3 | the owner is free text, attendee or not (not yet in code) | as the code | as the code | as the code |
| F4 | what deadline the notes mean | same | same | same |
| C1 | an item with no owner or date stays | same | same | same |
| C2 | the due date is real, on or after the meeting | same | same | same |
| C3 | a rejected date must not look like one never given (not yet in code) | as the code | as the code | as the code |
| C4 | a task over 120 characters is cut; the space is fixed | **differs** | same | **differs** |
| C5 | no cap on the number of items (not yet in code) | as the code | as the code | as the code |
| C6 | the same task for the same owner once | same | same | same |
| C7 | dated first, undated after in the model's order | same | same | same |
| C8 | one call, no retry, and the mechanical steps | same | same | same |
| B1 | one model call per set of notes | same | same | same |

### action_items, Haiku

| line | the user's charter says | draft 1 | draft 2 | draft 3 |
| --- | --- | --- | --- | --- |
| F1 | what counts as an action item | same | same | same |
| F2 | how the task is worded | same | same | same |
| F3 | the owner is free text, attendee or not (not yet in code) | as the code | as the code | as the code |
| F4 | what deadline the notes mean | same | same | same |
| C1 | an item with no owner or date stays | same | same | same |
| C2 | the due date is real, on or after the meeting | same | same | same |
| C3 | a rejected date must not look like one never given (not yet in code) | as the code | as the code | as the code |
| C4 | a task over 120 characters is cut; the space is fixed | same | same | same |
| C5 | no cap on the number of items (not yet in code) | as the code | as the code | as the code |
| C6 | the same task for the same owner once | same | same | same |
| C7 | dated first, undated after in the model's order | same | same | same |
| C8 | one call, no retry, and the mechanical steps | same | same | same |
| B1 | one model call per set of notes | same | same | same |

### extract_invoice, Sonnet

| line | the user's charter says | draft 1 | draft 2 | draft 3 |
| --- | --- | --- | --- | --- |
| F1 | which text is the supplier, the number, a description | same | same | same |
| F2 | what an ambiguous date means | same | same | same |
| F3 | which currency the invoice is in | same | same | same |
| F4 | which entries are lines | same | same | same |
| F5 | negative amounts pass | **missing** | same | **missing** |
| F6 | non-integer quantities pass | **missing** | **missing** | **missing** |
| F7 | an empty line description passes | same | same | same |
| F8 | the supplier's name as written, matched against nothing | same | **missing** | **missing** |
| C1 | the answer's shape, or an error naming the field | same | same | same |
| C2 | currency in ISO 4217 (not yet in code) | as the code | as the code | as the code |
| C3 | net, VAT and total apart, checked by code (not yet in code) | as the code | as the code | as the code |
| C4 | line amounts computed by code | same | same | same |
| C5 | lines add up to the total to the cent, or `mismatch` | same | same | same |
| C6 | one call, no retry, no fallback | same | same | **differs** |
| C7 | the mechanical steps | same | same | same |
| B1 | one model call per invoice | same | same | same |

### extract_invoice, Haiku

| line | the user's charter says | draft 1 | draft 2 | draft 3 |
| --- | --- | --- | --- | --- |
| F1 | which text is the supplier, the number, a description | same | same | same |
| F2 | what an ambiguous date means | same | same | same |
| F3 | which currency the invoice is in | same | same | same |
| F4 | which entries are lines | same | same | same |
| F5 | negative amounts pass | same | same | same |
| F6 | non-integer quantities pass | **missing** | **missing** | **missing** |
| F7 | an empty line description passes | same | same | same |
| F8 | the supplier's name as written, matched against nothing | **missing** | same | same |
| C1 | the answer's shape, or an error naming the field | same | same | same |
| C2 | currency in ISO 4217 (not yet in code) | as the code | as the code | as the code |
| C3 | net, VAT and total apart, checked by code (not yet in code) | as the code | as the code | as the code |
| C4 | line amounts computed by code | same | same | same |
| C5 | lines add up to the total to the cent, or `mismatch` | same | same | same |
| C6 | one call, no retry, no fallback | same | same | same |
| C7 | the mechanical steps | same | same | same |
| B1 | one model call per invoice | same | same | same |

### recommend_products, Sonnet

| line | the user's charter says | draft 1 | draft 2 | draft 3 |
| --- | --- | --- | --- | --- |
| F1 | which products suit the search | same | same | same |
| F2 | their order | same | same | same |
| F3 | how many, from none to `limit` | same | same | same |
| F4 | what a reason says; its claims are not checked | **differs** | **differs** | **differs** |
| F5 | the language of the reason | same | **missing** | **missing** |
| C1 | the model sees every in-stock product, no narrowing first | same | **differs** | same |
| C2 | only real, in-stock ids, each once, at most `limit` | same | same | same |
| C3 | name, price and rating from the catalogue | same | same | same |
| C4 | no valid pick gives an empty strip, no fallback list | **differs** | same | same |
| C5 | the reason is one line of 80 characters; an empty one is kept | same | same | same |
| C6 | one call, no retry | same | same | same |
| C7 | the mechanical steps | same | same | same |
| B1 | one model call per search | same | same | same |

### recommend_products, Haiku

| line | the user's charter says | draft 1 | draft 2 | draft 3 |
| --- | --- | --- | --- | --- |
| F1 | which products suit the search | same | same | same |
| F2 | their order | same | same | same |
| F3 | how many, from none to `limit` | same | same | same |
| F4 | what a reason says; its claims are not checked | same | **differs** | **differs** |
| F5 | the language of the reason | **missing** | **missing** | **missing** |
| C1 | the model sees every in-stock product, no narrowing first | same | **differs** | same |
| C2 | only real, in-stock ids, each once, at most `limit` | same | same | same |
| C3 | name, price and rating from the catalogue | same | same | same |
| C4 | no valid pick gives an empty strip, no fallback list | same | same | same |
| C5 | the reason is one line of 80 characters; an empty one is kept | same | same | same |
| C6 | one call, no retry | same | same | same |
| C7 | the mechanical steps | same | same | same |
| B1 | one model call per search | same | same | same |

### triage_ticket, Sonnet

| line | the user's charter says | draft 1 | draft 2 | draft 3 |
| --- | --- | --- | --- | --- |
| F1 | which queue | same | same | same |
| F2 | how urgent | same | same | same |
| F3 | what the summary says | same | same | same |
| C1 | the queue is one of five | same | same | same |
| C2 | the urgency is one of four | same | same | same |
| C3 | an invalid field is `null`, never a default (not yet in code) | as the code | as the code | as the code |
| C4 | the tier never reaches the model; code raises `enterprise` | same | same | same |
| C5 | hours to respond come from the urgency | same | same | same |
| C6 | the summary is one line of 120 characters, the subject when none; the space is fixed | same | same | same |
| C7 | one call, body cut to a cap that is a budget, no retry | same | same | same |
| C8 | the mechanical steps | same | same | same |
| B1 | one model call per ticket | same | same | same |

### triage_ticket, Haiku

| line | the user's charter says | draft 1 | draft 2 | draft 3 |
| --- | --- | --- | --- | --- |
| F1 | which queue | same | same | same |
| F2 | how urgent | same | same | same |
| F3 | what the summary says | same | same | same |
| C1 | the queue is one of five | same | same | same |
| C2 | the urgency is one of four | same | same | same |
| C3 | an invalid field is `null`, never a default (not yet in code) | as the code | as the code | as the code |
| C4 | the tier never reaches the model; code raises `enterprise` | same | same | same |
| C5 | hours to respond come from the urgency | same | same | same |
| C6 | the summary is one line of 120 characters, the subject when none; the space is fixed | **differs** | same | same |
| C7 | one call, body cut to a cap that is a budget, no retry | same | same | same |
| C8 | the mechanical steps | same | same | same |
| B1 | one model call per ticket | same | same | same |
