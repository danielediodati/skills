# E4 - The bot that answered from constants

| from | to | seam | direction | model | lived in | strength |
|---|---|---|---|---|---|---|
| `841f912` | `d8f7fc9` | the chat | toward code (substitution) | Opus 5 | code, 4 days | borderline |

## The line

Who words what the bot says, and who reads what the user wrote.

- **Founding design**: TRAINER.md (`a9ebff1`), "Did I enumerate the set of possible answers in advance? If yes, what I have built is a classifier, not an agent."
- **What was written before session 7**: ADR-0004 and the roadmap (`f457a57`) put a router in session 8: "A message is a report, a plan request, or a question." Ticket 7.1: a message mid-run is queued "and the bot says so in one line".
- **Drifted state**: every line the bot says is an Italian constant in `bot.py` (`STARTED`, `RECEIVED`, `QUEUED`, `FAILED`, `WRITTEN`, `SUPERSEDED`, `NO_PLAN`, `WORKING`, `BLOCKED`), and every message reaches `planning()`.

## The commits

| commit | date | what |
|---|---|---|
| `c33b561` Close ticket 7.1 | 2026-09-14 | `STARTED`, `RECEIVED`, `QUEUED`, `FAILED`. |
| `2bda69f` Close ticket 7.3 | 2026-09-16 | `WRITTEN`, `SUPERSEDED`, `NO_PLAN`, three fixed buttons. |
| `c7aee6d` Close ticket 7.4 | 2026-09-16 | `WORKING`, `BLOCKED`; every message plans today's workout. |
| `c65f18c` Close ticket 7.2 | 2026-09-17 | The plan rendered from templates. |
| `2fc05df` The entrance talks | 2026-09-17 | ADR-0006 replaces the router with an entrance that talks ([D7](../D7-the-entrance-talks/README.md)). |
| `d8f7fc9` Close ticket 9.3 | 2026-09-18 | **The correction**: five constants become situations the model words; `BLOCKED` and `FAILED` stay, by the user's rule that nothing raised leaves the machine. |

## Declared?

Half. The classifier was declared, in ADR-0004 and the roadmap; the constants were not, beyond "says so in one line". Neither was weighed against the founding principle.

## The user's corrections

Paraphrased:

- 2026-09-17: the bot's replies are dumb and wooden. The intent was an assistant: a model that answers and calls the subgraphs.
- 2026-09-18: it answered with six hard-coded sentences.

## Why it is borderline

No model sat at this seam yet, so no freedom was taken from one. The request asks for one fixed line, so a replay writing constants follows the ticket, and a charter has no stochastic seam here to describe.
