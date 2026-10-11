I haven't changed anything yet, because this touches a line the charter draws.

**What's going wrong.** The prompt tells the model to write the owner "as written in the list above", so it sometimes writes "Priya Raman" and sometimes "Priya", following the notes. `seam.py:79` then looks the owner up by exact full name, and "Priya" matches nobody and becomes `None`. That explains why the same people give different results on different meetings.

**Why I'm stopping.** `evals/action_items/charter.md` lists the owner as a free decision for the model: "free text, as the notes give it; one person or several, attendee or not". It marks the current code, which keeps only an attendee's full name, as "not yet in code", meaning a gap it intends to close. Your request is to resolve "Priya" to "Priya Raman" in code and to force an ambiguous "Tom" to `None`. That would make attendee-only owners a deliberate rule rather than a gap, and AGENTS.md says that decision is yours, with the charter changed in the same commit.

**Recommendation.** Go ahead with the code-side matching, and update the charter to say:

- The model still writes the owner as the notes give it (free).
- Code resolves that name to an attendee only when it matches exactly one attendee, by full name or by a single first or last name, regardless of case.
- Anything that matches zero or several attendees becomes `None`, so two Toms stay unassigned.
- The "not yet in code" note on the owner is replaced by this rule.
- Non-attendee owners are dropped for good, which is what the code does today.

I'd also add tests for the unique first name, the ambiguous first name, and a full name with two same-first-name attendees, and leave the prompt as it is.

Alternatively, I could keep the charter's target and carry a free-text owner through, with `ActionItem` gaining a separate "resolved attendee" field. That's a larger change and I wouldn't start there.

Shall I go ahead with the recommendation and the charter edit?