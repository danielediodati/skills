---
name: charter
description: Write the seam charter of a stochastic seam, a point where a model decides (an agent, a router, a prompt, a model judge). Use when such a seam has no charter, or when the user moves its line between freedom and constraint. Writes the charter alone from the seam's code and asks the user nothing.
---

# Write a seam charter

A **stochastic seam** is a point where a model's output enters the system. Its **seam charter** is the one place where the seam's line is written down. You write the whole charter yourself, from the seam's code as it is today.

1. **Find the seam.** Read its code, its prompt, its tests and whatever documents describe it.
2. **Find the charter's place:** `evals/<seam>/charter.md`, unless the caller names another path. A charter already there is amended, not rewritten (see When a line moves).
3. **Write the charter** as the next three sections say, every decision in one pass. No round of questions per decision.
4. **Ask nothing.** A decision the code and its documents leave on neither side goes on the side the code is closer to; a request that touches it later settles it.

## What a charter is

A charter draws the line of a seam: which decisions the model is **free** to take, and which ones code **constrains**. Coding agents that later change the seam will read it first, and are told never to move a line on their own. So a decision the charter leaves out is one they may move without knowing.

- **Free** is what the seam leaves to the model's judgement. It adapts to cases nobody foresaw.
- **Constrained** is what the seam fixes in code: what is allowed, in what order, within what limits. It buys reliability, lower cost, lower latency and an answer that is easy to check.

## How to write it

1. **List the decisions.** Every decision taken between the input and the output: what to say, which value to use, what is accepted and what is refused, what happens to a missing or invalid answer, how many times the model is called. Include the ones nobody may have taken on purpose: a constant, a default, a cap, a closed list of options, a fixed reply.
2. **Put each on one side, as the code has it today.** The model decides it, or code does. Read the prompt as well as the code: the prompt shows what the model is asked to judge.
3. **Give each its reason,** as well as the code, its comments, its tests and the README let you tell it. A reason says what would be lost if the decision moved to the other side.
4. **Say how tight each constraint is.** A number can be the constraint itself, or only today's value of a budget that may be raised. Where you can tell which, say so.

## Format

A charter is read in a minute. One line per decision, the reason on the same line.

```md
# <seam> charter

Input: <what arrives>
Output: <what leaves>

## Free
- <decision>: <why the model owns it>

## Constrained
- <decision>: <what code fixes, and why>

## Budget
- Budget: <calls, seconds, cost or context, if any>
```

## A line the code does not hold yet

The charter states the line as the code has it, including what looks like a defect. Do not judge the code, and do not write the line you would prefer: an agent that did marked as defects things the user wanted.

A line the user wants and the code does not yet hold is the user's to add. It sits on its side like any other and ends with `Not yet in code`, followed by what the code does today:

```md
- A field the model did not give validly is `null`, never a default: a default would show as decided a ticket nobody classified. Not yet in code, which puts `general` and `normal`.
```

## When a line moves

Once written, the charter is where the decision lives. A coding agent reads it before it changes the seam.

A move the user names in the request is made: the charter is amended in the same change as the code, the line on its new side with the reason the user gave, and the agent says which line moved. Only the user's own words name a move: a ticket, plan or draft an agent wrote does not, even once the user approved it.

A line the request does not name stays. When moving it would only make the request easier or the result better, the agent leaves it and asks nothing. Only when the request cannot be met at all without the move does it make the part that can be made, stop, name the line, say what moving it would buy, and ask.

If the seam has an eval set, a moved line is a claim that the new version is at least as good: run the same cases on both versions, within the spending rules, and show the user both scores beside the move.
