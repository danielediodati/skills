# AGENTS

## Agent skills

### Issue tracker

Issues live in the repo, as markdown files under `docs/work/<m>.<f>-<name>/issues/`, listed in `ROADMAP.md` under their feature and milestone, and named `<milestone>.<feature>.<ticket>`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Release

A change to what the plugin's skills tell an agent to do is measured before it ships. The feature that makes the change closes, as every feature does, without a tag; the measurement runs in `skills-eval` against its commit, and the milestone holding the change ships its version only once the measurement holds; `skills-eval` then takes the same tag, on the commit of the results it shipped on. If it does not hold, the change goes back to work, and nothing was released. The mistake behind it: 0.11.0 rewrote the rule `setup` writes and shipped with its README saying the rewrite was not measured yet.
