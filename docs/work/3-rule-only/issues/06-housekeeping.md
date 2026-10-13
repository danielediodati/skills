# Empty the open points of what is not open

Status: ready-for-agent
Blocked by: 04, 05

## What it produces

The last ticket of the session: `openpoints.md` keeps only what is undecided.

- **`CONTEXT.md` decision 2** loses "wrappers or optional references": it contradicts the rule that a skill names no skill of another collection. What stays: no fork, new skills live here.
- **An ADR on the central rule,** freedom and constraint held symmetrically, in place of the earlier one-way rule against code taking over. It is the choice a later reader would find least obvious.
- **The plugin loads:** `claude --plugin-dir <repo>/a4a` in a session, and the skills appear. Only the manifests have been validated so far. It costs nothing.
- **Known limits move to `CONTEXT.md`,** in a section of their own: the weak spots that are standing limits and not work to do (spotting drift in a diff takes judgement, a charter can go stale, the vocabulary is heavy, over-delegation has no real episode behind it, the process is heavy for a small project).
- **Parked items move to the end of `ROADMAP.md`:** other hosts, the candidate skills, the author's `roadmap` skill.
- **How to run the trials on this machine** moves beside the scripts it is about.

## Done when

- `openpoints.md` holds only points that wait for a decision or for work no ticket covers, and each says which.
- The ADR is in `docs/adr/`.
- The plugin has been loaded once, and what appeared is written in the commit.
