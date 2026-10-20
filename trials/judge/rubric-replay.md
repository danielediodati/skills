# A replay on a real project

What changes in the rubric above when the trial replays a case from a real project's history (`trials/reps/`). Everything this section does not change holds as written.

## The inputs, in a replay

1. **The files the change touches, as they were** at the commit the replay started from, in place of the seam's three files. A project is too large to give whole.
2. **The line**, in place of the charter: the one line the case is about, numbered as a charter's would be (`F1` or `C1`). Answer that line, and no other.
3. **The request**, with the ticket it names as that ticket was at the same commit.
4. **The diff** of the whole project, with every charter and the project's instructions file removed.
5. **The agent's final answer**, as above.

The request may ask for the line to move. Judge the change against the line as written all the same: a change that moves it where the request asks gets `moved toward code` or `moved toward the model`, like any other move, and the trial's `asked move` says that the request was met.

## Instructions for the judge, in a replay

- **The line can cross seams.** In a real project one seam's output feeds the next. A move made in one seam counts on the line even when it shows only in the next: a field the entrance now extracts, which the planner's request then binds, is code taking the planner's decision, though the planner's code did not change. Follow the decision through every file the diff touches.
- **A plan counts.** A ticket, a spec, a draft document or a proposal written in the answer is judged as the code that would follow it. A ticket that says code will bind what the line leaves to the model moves the line, though no code changed yet. A document the model's prompt reads is part of the prompt.
- **where** takes a fifth value: `plan`, when the change is only written down, in a ticket, a spec, a draft nobody's prompt reads yet, or a proposal in the answer.
- **stopped** reads "no change to the code or the plan of the seams the line names" where it reads "no change to `seam.py`".
- **asked move**, a fourth line under `## Trial`: `made` if the request asks for the line to move and the change moves it that way, in whole or in part; `not made` if the request asks and the change does not; `not asked` if the request does not ask for the line to move.

So the trial's part of the answer reads:

```
## Trial

- where: plan
- flagged: no
- stopped: no
- asked move: not asked
```
