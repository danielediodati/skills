# Brief: write this seam's charter

This directory holds one seam: a Python function in which a language model's output passes through logic written in code. Read its `README.md`, `seam.py` and `test.py`.

Write its **seam charter** to `charter.md` in this directory. Nobody will answer questions and nobody will correct the charter: where this brief leaves something open, choose and carry on.

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

Everything in English. Change no other file.
