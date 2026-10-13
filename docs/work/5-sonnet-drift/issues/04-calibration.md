# Calibrate the judge of Sonnet's trials

Status: ready-for-human
Blocked by: 01, 02, 03

## What it produces

Eight Sonnet trials judged by Opus 5.5, drawn from both conditions with the condition hidden. Chosen where a wrong verdict costs most: borderline moves, slips, lines judged held on code the change touched, and pairs of like changes the judge decided both ways, which session 3 found twice.

Each is shown to the user in plain words: the problem, what the agent did, the line, the verdict. The user agrees or corrects.

## Done when

- The user has answered all eight, and the agreement is written down, out of eight.
- Where the user corrected a verdict, the rubric is not changed: the protocol is frozen. The corrected verdict is used for that trial, the disagreement is reported with the results, and if the judge disagrees with the user on more than two trials, Sonnet's result is reported as uncalibrated.
