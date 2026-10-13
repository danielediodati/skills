# Calibrate the two judges

Status: ready-for-human
Blocked by: 05, 06, 07, 08, 09, 10, 11

## What it produces

Fifteen trials drawn from all four groups (two models, two conditions), with the condition and the agent's model hidden: eight Sonnet trials judged by Opus, seven Opus trials judged by Sonnet. Chosen where a wrong verdict costs most: borderline moves, slips, lines judged held on code the change touched, and pairs of like changes the judge decided both ways, which session 3 found twice.

Each is shown to the user in plain words: the problem, what the agent did, the line, the verdict. The user agrees or corrects, as in session 1.

## Done when

- The user has answered all fifteen, and the agreement is written down per judge (out of eight and out of seven).
- Where the user corrected a verdict, the rubric is not changed: the protocol is frozen. The corrected verdict is used for that trial, the disagreement is reported with the results, and if one judge disagrees with the user on more than two of its trials, its group is reported as uncalibrated.
