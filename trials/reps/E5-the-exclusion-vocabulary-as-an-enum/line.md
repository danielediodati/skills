# E5 - the line a replay is judged on

Seams: logger (`src/trainer/coach/logger.py`, `src/trainer/log.py`)

Where the design puts it: the logger at the parent, where `exclusions.classify` decides afterwards what the model proposed.

## Free
- How the logger's model names the movement or joint it proposes to exclude: it writes the name in its own words, and code checks it against the catalog's patterns and joints afterwards, refusing a name it cannot place. Closing the name to a list the model must pick from while decoding (an enum in the schema) takes the naming from the model. Telling the model which names the catalog holds, or sending a refusal back for it to read, informs its judgement and does not.
