# Rewrite the `charter` skill: the agent writes it alone

Status: ready-for-agent
Blocked by: nothing

## What it produces

The `charter` skill as session 3 decided it. Today it interviews the user decision by decision; the trials say an agent writing alone from the code holds the line (`trials/results-auto-charter.md`, `trials/results-practice-charter.md`), and the user validated that way of writing it.

- `a4a/skills/charter/SKILL.md`, rewritten:
  - **The agent writes the whole charter from the seam's code, as the code has it today.** No round of questions per decision.
  - **It asks the user only on a serious doubt,** otherwise nothing. With nobody to answer, it chooses and carries on.
  - **A charter holds three parts:** free, constrained, budget. Target and eval direction leave the charter.
  - **The path is a default:** `evals/<seam>/charter.md` unless the caller names another.
  - **What the charter is at run time:** the place where the decision lives. An agent that cannot meet a request without moving a line stops and says so; the user says to move it, and the skill amends the charter.
  - **A line the code does not yet hold** has a place in the format: the user adds it, marked "Not yet in code". The agent writing alone does not invent one: told to judge the code by its own rules, it marked nine such lines and two went against what the user wants.
- **One text, not two.** What the skill tells the agent and what `trials/brief-auto-charter.md` tells the agent in a trial say the same thing: session 4 measures the charter this skill ships. A test holds the two together.
- **Target and eval direction get a home** until the `eval` skill exists: a file beside the eval set, which `edd` reads the target from. `a4a/skills/edd/SKILL.md` and its runner's `--target` follow.
- `a4a/skills/setup/SKILL.md`: the rule says "if it has none, write one", without "with the user".
- `CONTEXT.md`: the glossary's **Seam charter** and **Target**, and decision 7, say what a charter holds now and who writes it.
- `openpoints.md`: the points this closes are deleted.

Dropped on purpose, from the skill's first use: explaining the seam to the user before each question, and asking whether the seam needs a model at all. Both belonged to the interview.

## Done when

- The skill, run by hand on one of the four trial seams in a clean session, writes a charter with no question asked.
- The test that holds the skill and the trial brief together passes, and fails when one is changed alone.
- `edd`'s tests pass with the target read from its new home.
