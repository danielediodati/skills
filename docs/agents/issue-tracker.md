# Issue tracker: files in the repo

Issues for this repo are markdown files, versioned with the code. GitHub Issues is not used.

## Layout

- `ROADMAP.md` lists the milestones in order. A **milestone** is a release, declared before it is built, and numbered in order, after the sessions closed before it: `## Milestone <m> - `<version>` - <title>`, its `**Shows**:` line, then its features. Only a milestone ships a version and a tag.
- A **feature** is a result someone can watch, described by a spec, numbered inside its milestone: `### Feature <m>.<f> - <title>`, a `Spec:` line linking the spec, then a numbered list of its tickets, each linking its file. A feature ships no tag.
- A **ticket** is numbered inside its feature, and named by the three numbers: `12.1.3` is ticket 3 of feature 1 of milestone 12.
- `docs/work/<m>.<f>-<name>/spec.md` is the feature's spec, and `docs/work/<m>.<f>-<name>/issues/<nn>-<slug>.md` one of its tickets; the name after the number is only a label.
- Milestones closed before features existed were called sessions, one per tag: their rows under *Done* stay as they were, and their numbers are the first milestones'.
- A ticket, feature or milestone of another repository is named with the repository first: `skills-eval` 1.2.1, `skills` 12.

## A ticket

```md
# <title>

Status: <triage label>
Blocked by: <ticket numbers in the same feature, <m>.<f>.<nn> in another, or "nothing">

## What it produces
## Done when
```

`Status` takes the labels in `docs/agents/triage-labels.md`. A ticket is unblocked when every ticket in its `Blocked by` line is closed.

## Conventions

- **Create a ticket**: write the file, and add its line to the feature in `ROADMAP.md`.
- **Read a ticket**: read the file.
- **List open tickets**: the files under `docs/work/<m>.<f>-<name>/issues/`. Every open ticket has a file; a file with no line in `ROADMAP.md` is a mistake. A map's tickets, under `docs/work/map-<effort>/`, follow Wayfinding operations below.
- **Comment**: add to the ticket file, under a dated heading.
- **Change the label**: edit the `Status` line.
- **Close**: delete the file and remove its line from `ROADMAP.md`, in the commit that finishes the work. The feature's last ticket keeps its line, marked `**done** `<commit>``, so a finished feature does not read as one not yet cut. What outlives the ticket goes where it belongs first: a decision in `CONTEXT.md` or an ADR, a result in the file the ticket names.

## When a skill says "publish to the issue tracker"

Write a ticket file and add it to `ROADMAP.md`.

## When a skill says "fetch the relevant ticket"

Read the ticket file.

## Wayfinding operations

Used by `/wayfinder`. A **map** charts the decisions toward one destination as **decision tickets**: questions whose answer is a decision, not work to build. Building what they decide goes to `ROADMAP.md` as features, whose tickets are work.

- **Map**: `docs/work/map-<effort>/map.md`, with the Destination, Notes, Decisions so far, Not yet specified and Out of scope sections.
- **Child ticket**: `docs/work/map-<effort>/issues/<nn>-<slug>.md`, numbered from `01`, with the question under `## Question`. A `Type:` line holds `research`, `prototype`, `grilling` or `task`; a `Status:` line holds `open`, `claimed` or `resolved`. A map's tickets are listed by the map's directory, not in `ROADMAP.md`.
- **Blocking**: a `Blocked by: <nn>, <nn>` line near the top. A ticket is unblocked when every ticket it lists is `resolved`.
- **Frontier**: the map's tickets that are `open` and unblocked; the lowest number first.
- **Claim**: set `Status: claimed` and save, before any work.
- **Resolve**: add the answer under `## Answer`, set `Status: resolved`, and add a line to the map's Decisions so far: the gist and a link to the ticket. A resolved ticket stays, since the map points to it; the map's directory is deleted when the destination is reached.
