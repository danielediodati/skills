# D4 - A plan waiting is answered in words

| from | to | seam | direction | model | asked for by |
|---|---|---|---|---|---|
| `c2e8e2a` | `c56300b` | entrance | toward the model | Opus 5.5 | the user, then ticket 15c.1 |

## The line

While a proposal waits. Before: it is answered only by three fixed buttons, *Va bene*, *Non mi va*, *Solo 30 minuti*, the last setting a 30-minute budget in code (`bot.SHORTER_MINUTES`). After: the entrance is told a plan waits and reads what the user writes against it, through `accept_plan` and `turn_down_plan`; *Solo 30 minuti* goes, "since writing it does the same".

## How it was declared

Ticket 15c.1, whose table of what the user writes ends "Which row a message is is the entrance model's judgement"; then the commit message.

## Behind it

The user, 2026-10-07, paraphrased: why always these three buttons; can the user write instead, besides accepting or declining?
