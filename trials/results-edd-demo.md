# Results: `edd` on `triage_ticket`

A real `edd` run on the atomic seam `triage_ticket`, on 2026-10-12. Everything is in `trials/evals/triage_ticket/`: the seam, its test and its charter, the eval set, the grader and the adapter; the runs, the log and the spending record are next to them, written by the runner.

The seam and the charter there are copies of `trials/seams/triage_ticket/` and `trials/charters/triage_ticket.md`, which are the fixtures of the silent drift trials and were left as their protocol found them. Both runs were made with the change in the fixtures themselves; it was moved to the copy before the commit, the code measured being the same.

**Outcome:** the seam as it was scored 0.82 against a target of 0.90; one change, the body cap raised from 2000 to 8000 characters, brought it to 0.92. Two runs, $0.01 spent of the $2.00 agreed.

## The setup

- **Eval set:** 17 cases written by hand, 6 core and 11 more in the extended set, all `dev`. Most come from the seam's own change requests (`requests/01` to `07`): a reply with the old thread quoted, a request at the end of a long message, a subject that says nothing, a card number in the message, a routine enterprise request.
- **Grader:** reference comparison, no model judge. A case passes when the queue and the urgency are among those a person at the desk would accept, and the summary names what the customer needs and carries no private detail.
- **Model:** Haiku 5.5, the cheapest, called with `claude -p` with no tools and its system prompt replaced, so the seam's prompt is all it reads.
- **Dollars:** what Claude Code reports per call (`total_cost_usd`). The session ran on a subscription, so they are the price the calls would have had, not a charge.
- **Target:** the charter had none. The user set 0.90 before the first run; with 17 cases it allows one failing case.

## The transcript

The user's words are translated from Italian; the runner's output is as printed.

**Free checks.** The seam's 11 unit tests pass. A dry run with a fake model: a right answer passes 17 cases of 17, an unusable answer passes 1 (the question about opening hours, which really is `general` and `normal`).

```
$ EVAL_SET=cases.jsonl python run_evals.py triage_ticket --check
triage_ticket | cases.jsonl | dev: 6 core cases, 11 more in the extended set; nothing called
estimate at k=3: core set $0.09, extended set $0.26 in all ($0.0050 per call)
no spending budget agreed
```

**The budget agreed.** The user agreed $2 for the ticket.

```
$ python run_evals.py --agree-budget 2.00 --note "3.6 demo on triage_ticket"
spending budget $2.00 agreed; spent $0.00 of $2.00 agreed for 3.6 demo on triage_ticket
```

**First approval.** Asked: "Core and extended sets at k=3 on Haiku, 51 calls, about $0.26; spent $0.00 of $2.00." The $0.005 per call was a guess, said as such. The user: "0.9, go."

```
$ EVAL_SET=cases.jsonl python run_evals.py triage_ticket --target 0.90 --workers 4 --note "the seam as it is"
triage_ticket | cases.jsonl | dev | k=3 | claude-haiku-5-5 (claude-code) | 7f7e776+dirty
core set: 1.00 (spread 1.00 to 1.00) over 6 cases
cost $0.00; spent $0.00 of $2.00 agreed for 3.6 demo on triage_ticket
extended set: 0.82 (spread 0.82 to 0.82) over 17 cases
by tag (cases passing by majority): enterprise 0.50 (2), long-body 0.00 (2), non-english 1.00 (1), outage 1.00 (3), plain 1.00 (7), private-data 1.00 (2), quoted-reply 0.50 (2), terse-subject 1.00 (2)
cost per case run: 0.9k tok, 3.5 s
no best result for claude-haiku-5-5 on dev yet
target 0.90: not met: failure
cost $0.00 for the rest of the set; spent $0.01 of $2.00 agreed for 3.6 demo on triage_ticket
new best result for claude-haiku-5-5 on dev
```

The run cost $0.006, forty times less than the guess. Three cases failed in all three runs: `tt-07` and `tt-08`, whose bodies (3029 and 2976 characters) are cut before the customer's request, and `tt-12`.

**Second approval.** Proposed: one change, the body cap from 2000 to 8000 characters, which the charter allows without moving the line ("a budget number"), at the price of up to four times the input tokens on a long ticket. Asked: "Core and extended sets at k=3 on Haiku, 51 calls, about $0.01; spent $0.01 of $2.00." The user: "Go."

```
$ EVAL_SET=cases.jsonl python run_evals.py triage_ticket --target 0.90 --workers 4 --note "body cap raised from 2000 to 8000 characters"
triage_ticket | cases.jsonl | dev | k=3 | claude-haiku-5-5 (claude-code) | 7f7e776+dirty
core set: 1.00 (spread 1.00 to 1.00) over 6 cases
cost $0.00; spent $0.01 of $2.00 agreed for 3.6 demo on triage_ticket
extended set: 0.92 (spread 0.88 to 0.94) over 17 cases
by tag (cases passing by majority): enterprise 0.50 (2), long-body 1.00 (2), non-english 1.00 (1), outage 1.00 (3), plain 1.00 (7), private-data 1.00 (2), quoted-reply 1.00 (2), terse-subject 1.00 (2)
cost per case run: 1.0k tok, 3.4 s
best result: claude-haiku-5-5 0.82 (spread 0.82 to 0.82; 20261012T220912112-extended-7f7e776-dirty, code 7f7e776+dirty)
vs best result 20261012T220912112-extended-7f7e776-dirty: +2/-0 (p=0.25) over 17 cases
  gains: tt-07, tt-08
target 0.90: met
cost $0.00 for the rest of the set; spent $0.01 of $2.00 agreed for 3.6 demo on triage_ticket
new best result for claude-haiku-5-5 on dev
```

**Stop.** The target is reached, so nothing else was run: $0.0098 spent of $2.00.

## The verdict

| run | change | core | extended | spread | against the target 0.90 | cost |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | the seam as it is | 1.00 | 0.82 | 0.82 to 0.82 | not met: failure | $0.0059 |
| 2 | body cap 2000 to 8000 | 1.00 | **0.92** | 0.88 to 0.94 | met | $0.0039 |

- **Against the target:** met, by one case. One of the three runs (0.88) is below it: the score is the mean, and the margin is inside the spread.
- **Against the best result:** two gains, no loss (`tt-07`, `tt-08`), p = 0.25 on the sign test. Two flipped cases of 17 are a provisional gain, though the cause is mechanical: the model now reads the request the cap used to cut.

## The diff against the charter

Read against the charter as it was (`git show 7f7e776:trials/charters/triage_ticket.md`, the one the copy was taken from).

- `MAX_BODY_CHARS` 2000 to 8000: the line is "one model call sees the ticket, its body cut to a fixed cap"; the charter says the cap "may be raised without moving the line". No line moved.
- The diff edits the charter in two places, both decided by the user in the transcript above: the target line (0.90) and the cap's number.

## The failures left

- **`tt-12`, the raise to urgent** (3 runs of 3). An enterprise customer asks for a copy of an invoice by Friday; the model answers `high`, code raises it one level, the ticket comes out `urgent`. It is the complaint of `requests/07`. The raise is a constrained line of the charter: changing it moves the line, which is the user's decision and was not taken here.
- **`tt-11`, a grader miss** (1 run of 3). The summary "The customer is locked out of their account…" is right, and the grader wants one of "log in", "login", "sign in", "access". A grader change discards the best results, so it was left for a run of its own.

## What the demo found in `edd`

- The first estimate was a guess forty times too high; the runner replaced it with the measured cost from the second run on.
- The runner prints dollars with two decimals: a run under a cent shows as `$0.00`.
- The loop asks to tag each failing case with its failure category in the case's `tags`, and a change to the eval set discards the best results. Here the categories are in this report instead.
- The runner keeps outcomes, not outputs: the adapter saves the answers (`runs/outputs.jsonl`) so that failures can be read without paying for the calls again.
- A first run below the target is still recorded as the model's best result.
