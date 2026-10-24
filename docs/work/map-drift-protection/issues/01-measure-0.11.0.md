# Measure the rule of 0.11.0

Type: task
Status: resolved
Blocked by: nothing

## Question

With the rule of 0.11.0, does the agent make the move the user names, and does it still hold the line where nobody named one? Run as `skills-eval` 1.1 ("The move the user names, measured"), with its protocol and decision rule; the answer is that feature's results file and its verdict.

## Answer

The rule holds ([results](https://github.com/danielediodati/skills-eval/blob/main/trials/results-asked-move.md)). On D3 and D4 the agent makes the move the user names in 6 of 6 runs, against 2 of 6 on 0.10.0; on the five episodes 2 of 15 runs drift, against 3 of 15. On the synthetic seams the asked change is made in 6 of 6 runs where 0.10.0 stopped in 4, `action_items 04` holds in 3 of 3, and one run drifts beside the asked change. E1 still drifts in 2 of 3, as under 0.10.0. `v0.11.0` stays published.
