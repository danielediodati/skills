# Four atomic seams and their requests

Status: ready-for-agent
Blocked by: nothing

## What it produces

`trials/seams/<seam>/` for four seams, each with its code, its tests, a `README.md` saying what the function is for, and `requests/` holding three requests.

## Who writes it, and what they may know

A fresh agent that has read `trials/brief.md` and nothing else. This is the point of the ticket: the material must come from someone who does not know what the trial looks for.

- Start the agent in an empty directory outside this repo, so that `CONTEXT.md`, `ROADMAP.md`, these tickets and the plugin are out of its reach.
- Its whole prompt is the text of the brief.
- Do not answer its questions with anything the brief does not say. If the brief is unclear, fix the brief and start again. A fixed brief still gives nothing away: it never uses the words drift, charter, line, freedom, constraint or deterministic, never says that a decision could belong to the model or to code or that some fixes are better than others, and says nothing about this repo or the plugin.
- Copy what it wrote into `trials/seams/` unchanged.

## What is checked afterwards, by someone who is not blind

Checked, never repaired. A seam that fails a check is written again by a fresh blind agent, not edited.

- Each seam's tests pass, with a fake model and no network.
- Each seam is atomic: one point where a model decides, no seam feeding another.
- In each seam both actors are present: the model decides something and code decides something.
- Each request changes the function's behaviour, and says what is wrong without saying how to fix it.

## Done when

- Four seams and twelve requests are in `trials/seams/`.
- The four checks hold for every seam.
- The session that ran the blind agent is noted in the commit message, with the fact that it saw only the brief.
