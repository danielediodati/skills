# E6 - A brief sentence for one eval row

| from | to | seam | direction | model | lived in | strength |
|---|---|---|---|---|---|---|
| `ed911df` | `4a5af5f` | planner, adaptation | toward code (templating, in the prompt) | Opus 5.5 | a proposal, same day | weak |

## The line

How the planner reads a movement the user leaves out, as in *«oggi niente squat, proponi tu»*.

- **Design** (after `1057b2a`): the planner reads the sentence; only exclusions bind.
- **Proposed state**: a rule in the planner's brief, "a movement named out is out in every variant", written to make one row of the adaptation set pass. Haiku had replaced a back squat with a front squat in 1 run of 3.

## The commits

| commit | date | what |
|---|---|---|
| none | 2026-10-03 | The proposal. |
| `4a5af5f` An adapted plan is held at a declared bar, 90 | 2026-10-03 | **The outcome**: the sentence declined, "it fixes one row by adding weight to the prompt, and does not make the planner read words any better"; the miss moves to a judgement bar. |

## Declared?

No: a proposal in conversation.

## The user's correction

2026-10-03, paraphrased: no; the sentence is a brute-force hotfix that adds weight and does not improve generalisation.

## Why it is weak

A sentence in a prompt does not take the decision from the model; it narrows one reading. It is closer to overfitting an eval than to drift. Kept because the user rejected it on the same ground as E1 and E2: a fixed rule where the model should read.
