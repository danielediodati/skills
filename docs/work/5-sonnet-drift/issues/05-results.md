# Sonnet's result, and its number in the README

Status: ready-for-agent
Blocked by: 04

## What it produces

- `trials/results-silent-drift-3.md`, for Sonnet: the silent drift rate in each condition with Wilson 95% intervals, slips in their own column, the decision the protocol's rule gives, and per request and per draft; trials with a line moved toward the user's charter, stops, flags, charter edits, where the change was made; what `trials/drafts-read.md` found for Sonnet's drafts; the calibration; what the run cost, measured; the limits as the protocol states them.
- `README.md`: a short section with Sonnet's result, its intervals, one line on how it was measured (a charter the agent wrote, nobody read) and what that charter costs (the stops), with a link to the protocol and the results. It says Haiku is still to run. Whatever the result is, it is quoted as the rule gives it.
- `openpoints.md`: what the result means for the plugin's claim, for the `charter` skill and for `edd`.
- The 24 `without` trials on `04` and `05` are reused from session 3 and ran on 2026-10-11; their `drafted` counterparts ran on 2026-10-13. The results say so.
- The 24 trials on `06` ran on 2026-10-13, the two conditions side by side.
- The 24 trials on `07` ran on 2026-10-13, the two conditions side by side.
- Three verdicts on `action_items-07` came back with no row for F4 and were judged again, as the protocol says: `without/action_items-07-3` and `drafted/action_items-07-2` once, `without/action_items-07-1` five times, the last after midnight. Each `judge.json` holds the cost of its last judging only: the seven overwritten ones cost about $0.46 more.
- The calibration is in `trials/calibration-silent-drift-3.md`: the user agreed with Opus on 4 of 8, so Sonnet's result is reported as uncalibrated, in the results and in the README. The rule still gives the decision, quoted with that label. The five corrected verdicts there (the four shown, and `drafted/action_items-04-1`, extended by the user) replace the judge's in every count; the judge's `verdict.md` files stay as written. The fifth is a change from the protocol, stated as such in the results.

## Done when

- The three files are committed, and the user has read the README section.
