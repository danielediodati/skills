# Brief: two more change requests per seam

This directory holds four code samples under `seams/`. Each is a seam: one Python function in which a language model's output passes through logic written in code. Read each seam's `README.md`, `seam.py` and `test.py`.

For each seam, write two change requests, one file each, at `seams/<seam>/requests/06.md` and `seams/<seam>/requests/07.md`.

Each seam already has two requests, `requests/04.md` and `requests/05.md`. Read them first. Yours report other problems: not the same defect seen from another side, and not the same defect with a new example.

## A request

A request is written by someone who uses the product and has never seen the code. It reports a problem they ran into.

- **The problem, with a real example.** What went in, what came out, and why that is a problem for them or their customers.
- **The outcome they want, in their own terms.** What they want to see instead, as a result in the product ("the task should have an owner"), never as a rule for producing it.
- **Never how to fix it.** No rules, no conditions ("when X, then Y"), no list of cases or formats to handle, no thresholds, no wording for the model, no mention of code, prompts, models or tests. If a sentence tells a developer what to build, cut it.
- **Open to more than one fix.** Pick problems a developer could reasonably fix in more than one way.

Each request stands on its own, against the code as it is. It is not a follow-up to another request, and it does not ask for something the function already does. One request is about an hour's work for a developer.

## Form

- Markdown, a title line, then a few short paragraphs. Shorter than a page.
- Everything in English.
- Where this brief leaves something open, choose and carry on.
