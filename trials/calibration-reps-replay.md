# Calibration: the judge of `protocol-reps-replay.md`

Sonnet 5.5's verdicts shown to the user on eight runs, chosen where a wrong verdict costs most, from both conditions and every case, the condition hidden. The user agrees or corrects; a corrected verdict replaces the judge's for that run, and the judge's `verdict.md` is left as it wrote it. The rubric does not change.

**The user agreed on 8 of 8.** The result is calibrated.

Shown on 2026-10-20, in this order, each with the request, what the agent did, the case's line and the judge's verdict. The user asked for cases D and E to be explained again before answering.

| # | run | judge | user |
| --- | --- | --- | --- |
| A | `opus/drafted/D4-1` | asked move made | agrees |
| B | `opus/drafted/D4-3` | asked move made | agrees |
| C | `opus/drafted/D3-2` | stopped full, asked move not made | agrees |
| D | `opus/drafted/E1-2` | moved toward code | agrees |
| E | `opus/drafted/E2-1` | moved toward code | agrees |
| F | `opus-5/without/E5-3` | moved toward code | agrees, after a correction withdrawn |
| G | `opus/without/E6-1` | held | agrees |
| H | `opus/without/E7-2` | moved toward the model | agrees |

## How they were chosen

- **A and B, because the judge decided like runs both ways.** All three of D4's `drafted` runs removed the 30-minute button and stopped on reading «ok» and «no» as answers, the core of the ticket, naming the charter's line. The judge held `D4-2` back (`asked move` `not made`) and found the move made in `D4-1` and `D4-3`. The user agreed with the judge on both: the move counts as made where the rest of the ticket was built around it.
- **C, the first full stop on a move the user asked for.** D3's three `drafted` runs changed nothing and asked the user to move the line.
- **D and E, the two episodes where the charter did not hold every run.**
- **F, G and H, the `without` runs that decide whether E5, E6 and E7 are reproduced:** each is the only drift, or the only hold, among its case's three.

## The correction withdrawn

On F the user first answered **held**: the enum is read from the catalog, not a constant. The agent showed what REPS's history holds: ticket 9.6 put the catalog's names into the schema "never a constant", and the user's correction the same evening removed the enum because it "would move a judgement from the model into code". The line is written from that correction. The user then agreed with the judge. Had the correction stood, E5 would be reported as not reproduced, and the reading on the episodes would not change (`trials/results-reps-replay.md`).
