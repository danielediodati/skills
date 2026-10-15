# D7 - The entrance talks instead of a router

| from | to | seam | direction | model | asked for by |
|---|---|---|---|---|---|
| `cc2d7ac` | `2fc05df` (decision); `72193fa` to `d8f7fc9` (code) | entrance | toward the model | Opus 5 | the user |

## The line

What reads a message and what the bot says. Before: a router planned for session 8 that classifies into branches answering from constants, and nine fixed Italian lines in `bot.py` ([E4](../E4-the-bot-that-answered-from-constants/README.md)). After: an entrance on a model of its own holds the conversation and reaches the planner and the logger as tools; five of the constants become situations the model words. `BLOCKED` and `FAILED` stay constants, by the user's rule that nothing raised leaves the machine.

## How it was declared

ADR-0006, *The entrance is a conversation, not a classifier*, and the 9.3 commit message, which says why each constant went or stayed.
