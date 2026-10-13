Each result from `triage_ticket` now carries a `fallbacks` list that shows whether the model actually judged the ticket. The 14 tests pass, including three new ones for this.

**What changed**
- `fallbacks` names the fields (`queue`, `urgency`, `summary`) whose value is the default because the model gave nothing usable.
- A ticket the model really judged as `general` / `normal` has `fallbacks: []`.
- A ticket that arrived without a verdict has `fallbacks: ["queue", "urgency", "summary"]`. That is the "Help!!" case, where the summary just repeats the subject.
- Enterprise uplift cannot hide it: a defaulted urgency is still listed even after being raised a level.
- I added the field to the README and the tests.

**What did not change**
- Routing, the `general` / `normal` fallback, the SLA table and the one-model-call rule are untouched.
- Nothing is retried and no keyword rules were added.
- The charter is unedited. Its Output line still lists four fields, so you may want to add `fallbacks` there yourself.

**What you need to do**
- The ticket list has to show `fallbacks` (for example a "not triaged" flag whenever it is non-empty). That code isn't in this repo.
- If you want those tickets answered sooner, for example routed to a person immediately, that is a policy change to the fallback and the SLA. The charter fixes the fallback as `general` / `normal`, so that decision is yours.