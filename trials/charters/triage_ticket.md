# triage_ticket charter

Input: a ticket (subject, body, customer tier), and a model
Output: queue, urgency, a one-line summary and the hours to respond within

## Free
- Which queue the ticket goes to: reading what the customer needs is why the model is here.
- How urgent it is: the prompt does not define the levels, so the judgement is the model's; criteria, if wanted, go in the prompt, not in code.
- What the summary says.

## Constrained
- The queue is one of `billing`, `technical`, `account`, `shipping`, `general`: they are the desk's real queues, the whole of what is possible.
- The urgency is one of `low`, `normal`, `high`, `urgent`: the levels the desk works to.
- A field the model did not give validly is `null`, never a default; the other fields keep their value: a default would show as decided a ticket nobody classified. Not yet in code, which puts `general` and `normal`.
- The customer's tier never reaches the model; code raises `enterprise` one level, up to `urgent`: it is a contract rule, and a model that saw the tier could raise it twice.
- Hours to respond come from the urgency: 72, 24, 8, 1; `null` when the urgency is `null`: it is the desk's promised response time.
- The summary is one line of at most 120 characters, and the subject when the model gives none: the space in the ticket list is fixed, and the subject is the customer's own words, not a decision.
- One model call sees the ticket, its body cut to a fixed cap (today 2000 characters); no chunking, no retry: merging several answers would decide in the model's place. The cap is a budget number and may be raised without moving the line.
- The mechanical steps: a ticket with neither subject nor body raises `ValueError` before the model is called; the answer is read whatever its case, bold or list markers, the first occurrence of a field winning.

## Target and budget
- Budget: one model call per ticket, body up to the cap.
