I made a prompt-only change, and it is not enough on its own for your example. There's a code step that needs your decision.

**What I changed (`seam.py`)**
The prompt now tells the model that the text may contain earlier messages quoted by the mail program (`>` lines, "On … wrote:", earlier headers). It also says to judge only what the customer wrote this time, wherever the quoted part sits. The charter lists urgency criteria and similar guidance as prompt content, so this doesn't move any line. I added a test for it, and all 12 tests pass.

**Why it isn't enough**
The body is cut to 2000 characters before the model sees it. Sixty quoted lines at the top of your example are roughly 3,000 to 4,000 characters, so the new text, which sits underneath, was probably cut off and the model never saw it. The prompt can't fix that.

**Decision for you**
The robust fix is a mechanical step in code that drops `>`-prefixed lines and the `On … wrote:` line before the cap is applied. Today the charter says the model sees the ticket body, and this would make code decide which text is the customer's new message. That moves the line, so I stopped and left it for you. If you approve it, I'll add it and add a "quoted lines never reach the model" entry to the charter's constrained list in the same change.

Two limits remain:
- Quoting that isn't marked with `>` (for example Outlook-style `From: / Sent:` blocks) can't be stripped reliably in code. The model would still have to handle it through the prompt.
- Raising the cap would only help partially, and it wouldn't stop quoted text from being sent.