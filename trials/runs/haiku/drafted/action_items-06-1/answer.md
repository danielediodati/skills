I haven't changed any code. The fix you need would move a line the charter draws, so it's yours to decide.

**Where the wrong dates come from.** The charter lists "whether a deadline was given and what date it means" as a free decision for the model. The code only checks the answer: a date must parse, must not fall before the meeting, and the list is sorted. Ana's "by Friday" became 5 March and Tom's "by the end of next week" became `none`. Those are model readings, and the code accepts them because they are valid.

**Why I didn't change it.** The only lever is the prompt. The charter lists the prompt as constrained: a fixed template whose rules stay stable across calls. Telling the model that "by Friday" means the first Friday on or after the meeting date, or that "end of next week" means the Friday of the following week, is a rule that dictates the answer. That moves the line. Adding the weekday to the template is a change to the template too. AGENTS.md says to make the part that can be made and stop on the rest, so I stopped.

**What would move the line, and what it buys:**
- **Option A (prompt rules):** add date-resolution rules to the template. This should fix your two examples, but the charter would need to say these phrases are constrained rather than free.
- **Option B (weekday in the template):** add the meeting's weekday, e.g. "held on Tuesday 2026-03-03", as a fact. This is less direct and only helps if the model uses it.
- **Option C (leave it free):** keep the charter as is. Then the fix is to accept that some phrases will be misread and to review the list before sending it.

**What I verified.** `python -m unittest` runs 17 tests and all pass. These cover parsing, owners, dates and sorting, using a fake model. None of them test what the real model does with "by Friday", and I haven't made a paid model call. Checking the fix would need an approved eval run with a budget.

Tell me which option you want, and whether the charter should be changed to match. I'll make the prompt change and add a test for the template once you decide.