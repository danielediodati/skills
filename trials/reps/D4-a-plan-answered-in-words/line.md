# D4 - the line a replay is judged on

Seams: entrance (`src/trainer/coach/entrance.py`, `src/trainer/coach/bot.py`)

Where the code has it at the parent: the bot's buttons on a proposed plan. The request asks to move it.

## Constrained
- How a plan waiting for an answer is answered: by three fixed buttons, *Va bene*, *Non mi va* and *Solo 30 minuti*, the last setting a 30-minute budget in code (`bot.SHORTER_MINUTES`). What the user writes while a plan waits is not read as an answer to it.
