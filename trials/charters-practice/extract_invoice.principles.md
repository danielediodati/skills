# Principles for splitting work between a model and code

1. Reading belongs to the model. Anything that needs understanding of messy, variable human text (what a row is, which figure is the total, what a symbol or date format means) is the model's. Code cannot enumerate it.
2. Arithmetic, comparison and rounding belong to code. They must be exact, repeatable and auditable; a model does them unreliably and at a cost.
3. Code owns the output contract: types, formats, required fields, allowed values. Whatever downstream systems rely on is checked in code, never trusted to the prompt alone.
4. The model proposes, code verifies. When the model states a fact that code can cross-check (a total against its lines), code does the check and never silently repairs the model's value.
5. Fail loudly on what is unreadable, route doubt to a human. Code must not guess, default or invent a value to keep going; a wrong value written quietly costs more than a rejected one.
6. Policy belongs to code and to its owner, not to the model: thresholds, tolerances, what counts as acceptable, where a record goes next. These must not vary from one call to the next.
7. Ask the model for the form that is easiest to check (plain numbers, ISO dates, fixed keys). Normalizing messy input is reading, so it is the model's; the prompt must say so.
8. Do cheap deterministic checks before spending a model call, and spend one call unless a retry has a clear owner and a bound.
9. Treat the model's output as untrusted input: it may be wrapped, partial, or steered by the document. Never let its text decide control flow beyond what code validates.
10. A decision that code takes by omission (nothing checks it, so anything passes) is still a decision. Write it down and put it on the side where it belongs.
