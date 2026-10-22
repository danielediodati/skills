# 2. The evals live in a repository of their own

## Context

Through session 7 the trials lived in `trials/`, beside the plugin: protocols, briefs, the four synthetic seams, REPS's cases, 8.6 MB of raw runs, the judges, the tallies and their results. The plugin itself is under 100 KB. Scripts in `trials/` read the plugin's skills from the same tree, so a result measured whatever the working copy held, and nothing pinned it to a release.

## Decision

The trials move to [`skills-eval`](https://github.com/danielediodati/skills-eval), with their git history, so every protocol keeps the commit that dates it before its first paid call. The plugin is a submodule there, pinned at the tag a result measured; every number in this README links to a result at a tag of `skills-eval`.

Each repository holds the files of its own purpose: roadmap, open points, vocabulary, decisions. An item goes where its closing changes something: a decision about what the plugin does stays here, even when its evidence is in `skills-eval`; a question about how drift is measured goes there. A session that changes the plugin and measures the change is two sessions: the change here first, then the measurement there, against the tag the change shipped.

## Why

- **The plugin ships what it needs.** Installed from the marketplace, it comes as a shallow clone of this repository: without the trials, it carries no run.
- **A result names what it measured.** A submodule at a tag says which plugin produced a number; a sibling folder says only that it was nearby.
- **The preregistration survives the move.** Extracting the history, not copying the files, keeps the date of every protocol before its runs.

## Considered

- **Leaving the trials here.** One repository, one commit per ticket. Set aside: every install carries the runs, and nothing pins a result to a release.
- **Rewriting this repository's history without `trials/`.** Set aside: it is public, and its tags and links are already out. Deleting `trials/` in an ordinary commit is enough for an install.
- **One roadmap for both, here.** Set aside: an item belongs where it is closed, and most measurements close in `skills-eval`.

## Consequences

- A ticket that changes the plugin and its measurement no longer closes in one commit.
- Moving the submodule to a new tag is the start of a measurement, never a side effect.
- The plugin's README cites results by tag of `skills-eval`, and a new result means a new tag there before the README here can cite it.
