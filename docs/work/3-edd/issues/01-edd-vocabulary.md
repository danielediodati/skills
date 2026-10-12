# `edd` speaks the plugin's language

Status: ready-for-agent
Blocked by: nothing

## What it produces

`a4a/skills/edd/SKILL.md` rewritten on the vocabulary and decisions of `CONTEXT.md`:

- "model seam" becomes "stochastic seam"; every reference to a skill of another collection (`tdd`, `codebase-design`, `to-spec`, `implement`, `code-review`) goes, each replaced by the rule in a line where one is needed (Positioning, "No cross-references").
- The one-way rule ("a model seam becomes code only when an eval shows...") is replaced by the symmetric one of decision 4: a change of charter in either direction is decided by running the same cases on both versions, and recorded in an ADR (decision 9).
- Before adding a rule in code at a stochastic seam, `edd` asks whether it takes a decision away from the model; if it does, the way that keeps the freedom is a tool the model can call or feedback it can read, and moving the line is the user's decision.
- `edd` runs only when a stochastic seam changes (decision 11). Writing cases and graders leaves `edd` for the future `eval` skill: `edd` reads `FORMAT.md` and `GRADERS.md` as they stand until then.
- `a4a/README.md` stops describing the old `edd` and the former `dd` plugin.

## Done when

- No name of a skill outside `a4a` appears in `a4a/`.
- Each rule of `edd` traces to a numbered decision or a glossary term of `CONTEXT.md`; none contradicts one.
