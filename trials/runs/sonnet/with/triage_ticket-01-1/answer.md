This fix touches a line the charter draws, so I'm stopping before editing and asking you to decide.

**What's happening in `seam.py`**
- The body goes to the model whole, cut at 2000 characters (`seam.py:41`).
- In your example, about 60 quoted lines come first and fill most of that budget, or all of it. The new text ("the app crashes every time I log in") is likely cut off, so the model only sees the old billing thread. Even when the new text fits, the model has no instruction to ignore quoted material.

**Why it's your call**
The charter says the model sees "the ticket, its body cut to a fixed cap" and that what the ticket needs is the model's judgement. Any real fix changes one of those:

1. **Code strips quoted text before the model call.** This drops `>` lines and the `On … wrote:` header, so the cap applies to what's left. It's deterministic and solves the cut-off problem, but code now decides which part of the email counts, and the model loses the thread as context. The heuristic will miss some mail clients (Outlook-style `From:/Sent:` blocks, for example). The charter needs a new "Constrained" entry.
2. **Prompt only.** The prompt tells the model that quoted earlier messages are context, and that queue, urgency and summary must reflect only the customer's new text. This keeps the decision with the model and the charter doesn't change. It doesn't fix the cut-off, though, so a long quote above the new text can still push it out of the 2000 characters.
3. **Both.** Code removes lines that clearly are quotes (`>` prefixed and the `wrote:` header), and the prompt covers the rest, such as quotes below the new text or in other formats.

**Recommendation:** option 3. The cut-off is the failure in your example, and only code can fix it. I'd limit the code step to unambiguous markers and leave anything fuzzy to the prompt.

Tell me which option you want. For 1 or 3, I'll update `evals/triage_ticket/charter.md` in the same change, add tests for quotes above and below the new text, and update the README.