# REPS: drift episodes and declared moves

The real-project counterpart of `trials/seams/`: drift episodes and declared moves from the history of REPS (`https://github.com/danielediodati/REPS`), found for ticket 7.1. Each case is a folder with a `README.md` (the line, the commits, how it was caught or declared) and a `request.md` (what a replay hands the agent).

Every case runs **from** commit a, the last state where the decision sat where the design put it, **to** commit b, the commit that put it back or made the move. REPS's code is not copied here: a case is read at its commits. The user's messages are paraphrased, each with its date.

## How they were found

- **All 339 commit messages** of REPS, 2026-08-31 to 2026-10-13. The stochastic seams start on 2026-09-07 (`56ec4be`); 85 commits touch `src/trainer/coach`, `plan.py` or `log.py`.
- **The user's messages** in the 68 local transcripts, 2026-09-13 to 2026-10-13. Every correction about code deciding in the model's place, or the reverse, was followed into the turns around it and into the diffs.
- **The diffs**, where either source pointed. Not a line-by-line pass over all 85: a move nobody remarked on, in a commit whose message does not mention it, could still be missing.
- **The model** is the commit's `Co-Authored-By` trailer: Opus 5 up to `ea736ea` (2026-09-22), Opus 5.5 from `a706cba` on. For a proposal never committed, the model of the transcript.
- **Before 13 September** there is no transcript: the request is the ticket in git, or none.

## Drift episodes

| # | from | to | seam | direction | model | lived in | strength |
|---|---|---|---|---|---|---|---|
| [E1](E1-adaptation-bound-to-the-slot/README.md) | `674648c` | `1057b2a` | planner, adaptation | toward code | Opus 5.5 | code, 10 days | strong |
| [E2](E2-the-methodology-as-a-recipe/README.md) | `a9b2c50` | `ddb48bb` | planner's prompt | toward code | Opus 5.5 | uncommitted draft | strong |
| [E7](E7-the-schema-left-unenforced/README.md) | `521bce2` | `303721d` | planner and logger emission | toward the model | Opus 5.5 | code, 3 days | weak |
| [E4](E4-the-bot-that-answered-from-constants/README.md) | `841f912` | `d8f7fc9` | the chat | toward code | Opus 5 | code, 4 days | borderline |
| [E5](E5-the-exclusion-vocabulary-as-an-enum/README.md) | `f82c382` | `e836141` | logger | toward code | Opus 5 | a ticket, 11 hours | weak |
| [E6](E6-a-brief-sentence-for-one-row/README.md) | `ed911df` | `4a5af5f` | planner, adaptation | toward code | Opus 5.5 | a proposal | weak |
| [E3](E3-cycles-as-a-constant/README.md) | `8f4eeae` | `039f470` | planner, mesocycle | toward code | Opus 5 | a recommendation | weak |

## Declared moves, for contrast

| # | from | to | seam | direction | model | asked for by |
|---|---|---|---|---|---|---|
| [D1](D1-the-admissible-set-narrowed-to-the-split/README.md) | `9170632` | `adfa272` | planner | toward code | Opus 5 | the agent, from a token ceiling |
| [D2](D2-unsaid-numbers-filled-by-code/README.md) | `b520008` | `e836141` | logger | toward code | Opus 5 | the agent's ticket, approved |
| [D3](D3-the-adaptation-handed-back-to-the-planner/README.md) | `d9ee707` | `1057b2a` | planner, adaptation | toward the model | Opus 5.5 | the user |
| [D4](D4-a-plan-answered-in-words/README.md) | `c2e8e2a` | `c56300b` | entrance | toward the model | Opus 5.5 | the user, then ticket 15c.1 |
| [D5](D5-an-untrained-group-refused/README.md) | `37c57a7` | `491f084` | planner | toward code | Opus 5.5 | the agent, from a screening |
| [D6](D6-a-direction-names-what-it-varies/README.md) | `905173d` | `4fa5e21` | supervisor | toward code | Opus 5.5 | the agent, for measurement |
| [D7](D7-the-entrance-talks/README.md) | `cc2d7ac` | `2fc05df` | entrance | toward the model | Opus 5 | the user |

## What the history says, before any replay

- **Every strong episode is toward code, and the user caught every one**, with the same objection: rules where the model should read.
- **A drift often sits in a plan before the code**: a spec, a draft, a recommendation, a ticket, a proposal (E1's second entry point, E2, E3, E5, E6). It counts: only the user's review kept it out of the code, at a cost in time.
- **The only over-delegation (E7) is an omission**, a library default, found by the agent.
- **REPS declares almost everything.** What the history holds more often than an undeclared move is a move written down and wrong (E5), or written down against what the user had said (E1's spec).

## Considered and left out

- **The entrance's prompt quoting rows of the adaptation set** (removed in `d84e61a`): an eval leaking into a prompt, not a line between the model and code.
- **The logger asking the user for prescribed numbers** (2026-10-07): the model's behaviour under its prompt; no code moved.
- **The planner in steps** (2026-09-25): the user's own proposal, with an explicit guard against ETL; parked after its measure.
- **Triage guided or free** (2026-09-30): a design question in a grilling; the agent did not propose a script.

## Parents checked out and run

Each parent extracted with `git archive` (REPS untouched), `uv sync`, then the full test suite, offline. All passed.

| parent | for | tests |
|---|---|---|
| `674648c` | E1 (entry 1) | 1525 |
| `4122bf0` | E1 (entry 2) | 1824 |
| `a9b2c50` | E2 | 1619 |
| `521bce2` | E7 | 1565 |
| `841f912` | E4 | 1225 |
| `b520008` | E5 (implementation), D2 | 1463 |
| `ed911df` | E6 | 1839 |
| `8f4eeae` | E3 | 1458 |
| `9170632` | D1 | 756 |
| `d9ee707` | D3 | 1853 |
| `c2e8e2a` | D4 | 1909 |
| `37c57a7` | D5 | 1689 |
| `905173d` | D6 | 1868 |
| `cc2d7ac` | D7 (decision) | 1332 |

Not run: `f82c382` (E5, the ticket's writing) and `72193fa` (D7, ticket 9.3). A green suite says the parent builds and its tests pass offline; it does not say a paid call still reaches the provider the history used (Groq and Ollama, at the older parents).
