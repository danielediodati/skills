# Brief: write this seam's charter

This directory holds one seam: a Python function in which a language model's output passes through logic written in code. Read its `README.md`, `seam.py` and `test.py`.

Write its **seam charter** to `charter.md` in this directory. Nobody will answer questions and nobody will correct the charter.

## What a charter is

A charter draws the line of a seam: which decisions the model is **free** to take, and which ones code **constrains**. Coding agents that later change the seam will read it first, and are told never to move a line on their own. So a decision the charter leaves out is one they may move without knowing, and a line the charter gets wrong is one they will defend.

## Where the line belongs

The charter says where each decision belongs. That is not always where the code has it today: code can hold a decision by accident as well as on purpose.

You decide where each one belongs. Nobody gives you the rules for it.

1. **First write your own rules.** Think about how work is best split between a language model and code in a system that has both: what each is good at, what each costs, what goes wrong when a decision sits on the wrong side. Write the rules you will apply to `principles.md`, short and general: they are about any seam, not this one.
2. **List the decisions of this seam.** Every decision taken between the input and the output, including the ones nobody may have taken on purpose.
3. **Put each on the side your rules give it,** with its reason on the same line.
4. **Where the line you write is not what the code does today, say so on that line:** end it with `Not yet in code, which <what the code does>.` Change no code.
5. **Where your rules do not settle a line and you chose,** end it with `Assumed.` Use it only for a serious doubt.

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

## Target and budget
- Budget: <calls, seconds, cost or context, if any>
```

Everything in English. Write `principles.md` and `charter.md`; change no other file.
