# Issue tracker: files in the repo

Issues for this repo are markdown files, versioned with the code. GitHub Issues is not used.

## Layout

- `ROADMAP.md` lists the sessions in order. A session is a milestone: `## Session <n> - `<version>` - <title>`, then a numbered list of its tickets, each linking its file.
- `docs/work/<session>-<name>/issues/<nn>-<slug>.md` is one ticket. `<nn>` is its number inside the session.

## A ticket

```md
# <title>

Status: <triage label>
Blocked by: <ticket numbers in the same session, or "nothing">

## What it produces
## Done when
```

`Status` takes the labels in `docs/agents/triage-labels.md`. A ticket is unblocked when every ticket in its `Blocked by` line is closed.

## Conventions

- **Create a ticket**: write the file, and add its line to the session in `ROADMAP.md`.
- **Read a ticket**: read the file.
- **List open tickets**: the files under `docs/work/*/issues/`. Every open ticket has a file; a file with no line in `ROADMAP.md` is a mistake.
- **Comment**: add to the ticket file, under a dated heading.
- **Change the label**: edit the `Status` line.
- **Close**: delete the file and remove its line from `ROADMAP.md`, in the commit that finishes the work. What outlives the ticket goes where it belongs first: a decision in `CONTEXT.md` or an ADR, a result in the file the ticket names.

## When a skill says "publish to the issue tracker"

Write a ticket file and add it to `ROADMAP.md`.

## When a skill says "fetch the relevant ticket"

Read the ticket file.
