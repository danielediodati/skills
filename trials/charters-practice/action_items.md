# action_items charter

Input: free-text meeting notes, the attendee names, the meeting date, and a model (prompt string in, string out).
Output: at most 10 `ActionItem(task, owner, due)`, ordered by deadline with undated items last; owner is an attendee as the caller spelled it or `None`, due is a real date on or after the meeting or `None`.

## Free
- What counts as an action item: the model reads the notes and separates commitments from decisions, opinions and things already done; this is reading meaning.
- Who took it: the model decides which attendee a commitment belongs to, including resolving "I", "we", first names and pronouns against the notes, and answering "none" when nobody took it.
- Which day was meant: the model turns "Friday the 6th", "end of next week" or "after the launch" into a date or "none"; this is interpreting language.
- How the task is worded: the model writes the short imperative sentence, in whatever language the notes use.
- Whether two lines are the same commitment in different words: the model should write one item per commitment; paraphrase detection is not done in code.

## Constrained
- Whether to call the model at all: blank notes return `[]` without a call, since there is nothing to read.
- The calendar facts the model needs: code supplies them in the prompt, since weekday arithmetic is what models get wrong. Not yet in code, which gives only the ISO meeting date and no weekday.
- The answer format `task | owner | due`: code parses it, tolerates bullets, numbering, stray spacing and quotes, splits from the right so a task may contain `|`, and skips every other line (chatter, echoed header, wrong field count, empty task); the consumer needs a fixed shape. A skipped line that held a real commitment is lost without a trace.
- Owner is one of the attendees: code matches the model's text to the attendee list ignoring case and spacing and returns the caller's spelling; anything else becomes `None` and the item stays, because ownership must be checkable by the tracker and an item with an unknown owner is better than none. The match is exact, so a bare first name from the model becomes `None`; the prompt asks for names as listed, which is where that is fixed.
- Deadline is a real date not before the meeting: code parses ISO dates and sets `due` to `None` for anything unparseable, impossible or earlier than the meeting day (the meeting day itself is kept), since that is a calendar check. A wrong but plausible date passes unseen.
- Exact duplicates are listed once: code drops a repeat of the same normalised task for the same owner, keeping the first. Not yet in code, which also merges two different owners the model wrote who both resolve to `None`, and may keep the first copy's missing due date over a later copy that has one.
- Task length is at most 120 characters: code cuts at a word boundary and adds `…` because consumers need a bounded field. Not yet in code, which never tells the model the limit, so the cut is the only thing that enforces it.
- Order is by deadline, undated last, undated in the model's order: code sorts, since order is a rule and not a judgement.
- At most 10 items, keeping the earliest deadlines: code truncates, since consumers need a bounded list. Assumed. Not yet in code, which never tells the model the cap, so items past ten are dropped silently.
- Failures of the model call itself: no retry and no catch; an exception from `model` reaches the caller, who owns the policy for it.

## Target and budget
- Budget: one model call per request, no retries; the whole trimmed notes text goes in one prompt with no length limit or chunking.
