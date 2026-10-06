---
name: charter
description: Write the seam charter of a stochastic seam, a point where a model decides (an agent, a router, a prompt, a model judge). Use when such a point is being designed or specified, when its charter is missing, or when someone wants to move its line between freedom and constraint.
---

# Grill a seam

A **stochastic seam** is a point where a model's output enters the system. Its **seam charter** draws the **line**: which decisions the model is free to take, which ones code constrains, and why. The rule the charter exists to hold: where there is freedom, freedom stays; where there is a constraint, the constraint stays. The line moves only when the user decides it.

Looking things up is your job; deciding is the user's. Read the spec and the code for facts, and put every decision to the user.

## Steps

1. **Find the seam.** Name it and state its input and its output in one line each. If `evals/<seam>/charter.md` exists, read it: this session amends it. Read whatever spec or code the seam already has.

2. **List the decisions.** Write down every decision taken between the input and the output: what to say, which tool to call, in what order, which value to use, when to stop, when to ask. Include the ones nobody took on purpose: a constant, a default, a closed list of options, a fixed reply. Done when every decision between input and output is on the list.

3. **Grill the line.** Put each decision to the user: free or constrained? Ask in rounds, numbered, each with your recommendation and its reason for this system. Neither side is the default. Say what each side buys here:
   - **Free** adapts to cases nobody foresaw.
   - **Constrained** buys reliability, lower cost, lower latency and an answer that is easy to check.

   Two tests help the user decide. A decision whose right answer can be written down before running anything (arithmetic, membership in a set, a format, a permission) can live in code. A decision that a function could take only by losing something belongs to the model.

   Two shapes need the user's explicit word, because they look like constraints and often are not:
   - **A closed list the model picks from.** A constraint when the list is everything that is possible (the valid ids). A template when the list is a menu of someone's taste (three styles).
   - **A fixed reply.** A constraint when the model is absent or cannot be trusted there (a crash, a refused permission). Otherwise the model's voice replaced by a string.

   Done when every decision sits on one side with a reason the user gave or accepted.

4. **Target and budget.** Ask for the target, a score on the seam's eval set ("held-out pass rate at least 0.80"), and for a budget wherever the system has one (calls, seconds, cost, context). The target is a declared goal: the first eval run may show it was wrong, and only the user corrects it.

5. **Eval direction.** Agree the rules the eval set will follow, in four lines. Rules only; the cases and graders are written later, from these.
   - **Good**: in words, what makes an output good where the seam is free.
   - **Broken**: what violating each constraint looks like.
   - **Cases come from**: the sources, most valuable first (real failures, then the edge cases this session raised).
   - **Held-out axis**: what the held-out cases differ on (a new user, a new repository, a new domain).

6. **Write the charter** to `evals/<seam>/charter.md` in the format below and show it to the user. Done when the user confirms it.

Amending a charter whose seam already has an eval set: a moved line is a claim that the new version is at least as good. Run the same cases on both versions, show the user both scores, and amend the charter after they choose.

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
- Target: <score on the eval set>
- Budget: <calls, seconds, cost or context, if any>

## Eval direction
- Good: <what makes a free decision good>
- Broken: <what violating each constraint looks like>
- Cases come from: <sources, most valuable first>
- Held-out axis: <what held-out cases differ on>
```
