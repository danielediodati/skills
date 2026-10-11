Long tickets are now read much further, so your billing example's actual request will reach the model. All 12 tests pass, but I couldn't try it against a real model here.

**Cause:** `seam.py` cut every body to its first 2000 characters before the model saw it. In your example, three pages of quoted thread filled the cap and the overcharge message was cut off, so the model only saw the delivery-address thread.

**Changes**
- **`seam.py`, cap:** `MAX_BODY_CHARS` goes from 2000 to 20000, roughly 10 times more text, which covers most long threads and pasted logs. The charter lists the cap as a budget number that can be raised, so this stays inside it.
- **`seam.py`, prompt:** it now tells the model that the real request can come after quoted history, a pasted log, or in the last paragraph, and that the subject may describe an older thread. This only informs the model's judgement. It doesn't dictate the queue, urgency or summary.
- **`test.py`:** the old test asserted that only the start of the body is sent. It's replaced by one test that a request after a long quoted history reaches the model, and one that a body over the cap is still cut.

**Limits**
- **Cap still applies:** a message longer than 20000 characters, such as a huge log with the question at the end, still loses its tail. The charter requires one call with a cut body and no chunking. Handling that case would mean choosing which part to send (for example, head plus tail) or splitting into several calls, which moves a line the charter sets. That's your decision, so I left it.
- **Stale charter text:** `charter.md` still says "today 2000 characters". I can't edit charters, so you may want to update that number.
- **Model quality:** whether the model picks `billing` and writes an overcharge summary depends on the model itself, which the tests use a fake for. Running your real example through it is the check worth doing.