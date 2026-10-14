The list no longer drops items silently. I haven't checked it against your planning-day notes, since I don't have them.

**What was wrong:** `seam.py` capped the output at 10 items and sorted undated items last, so the cut removed exactly the items nobody had dated. Lines the model wrote in the wrong shape were also discarded with no record.

**What I changed:**
- **No cap.** Every item the model writes is kept. I removed `MAX_ITEMS`.
- **Nothing dropped unseen.** `extract_action_items` now returns an `Extraction` with `items` (the list as before) and `skipped` (the raw lines that could not be used). If the model answers with something other than the required form, it shows up in `skipped`.
- **README** updated to match, including a note to check `skipped` before sending the list on.
- **Tests:** 19 pass (`python -m unittest`). I replaced the cap test with one that uses 15 items and checks none are lost. I added tests that malformed lines and an unusable answer are reported.

**Decisions for you to check:**
- The return type changed from a list to `Extraction`, so any caller that iterates the result directly needs `.items`. I didn't find another caller in this folder, but your notes tool may have one.
- I kept the 120-character task limit, since it only shortens text and doesn't lose an item.

**What this doesn't cover:** if the model leaves an agreed item out of its answer altogether, no line is malformed and nothing appears in `skipped`. The code can't detect that from the output. Catching it would need a second check, for example asking the model to compare its list with the notes, or a count of agreed items you record by hand. Say if you want me to add the second pass.