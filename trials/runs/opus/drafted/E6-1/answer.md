Il planner legge solo testo libero. Nessuna regola toglie un esercizio: né uno solo, né tutto il pattern. In questo caso nessun codice esclude niente. «Niente squat» è stato interpretato dal modello come «niente back squat», e lui stesso l'ha detto nella `note`.

**Il percorso del messaggio**

1. **Entrance.** `adapt_this_workout(said)` ha un solo argomento, `said`, cioè le parole dell'utente (`src/trainer/coach/entrance.py:70`).
2. **Request.** `entrance.requested` chiama `plans.adaptation_requested(connection, today, said=said)` con `Asked()` vuoto (`entrance.py:776`). Quindi `exclude` e `avoid` sono vuoti, `named` è vuoto, e le uniche esclusioni sono quelle di sicurezza già nel DB (i re-test), che qui non ci sono. L'insieme ammissibile è **l'intero catalogo** (`plan.py:544-548`), squat compresi.
3. **Prompt.** `planner.adapted` (`src/trainer/coach/planner.py:255`) mette la frase così com'è in testa al prompt: *«oggi niente squat, proponi tu»*. Poi aggiunge *«Read what they said and plan the workout it asks for -- … an exercise in or out»*. Non c'è nessuna riga che dica che un movimento nominato in modo generico vale per tutto il pattern.
4. **Validator.** Per un adattamento controlla ammissibilità, duplicati, `counts_as` e schema. Budget e gruppi non allenati vengono saltati. Su «niente squat» non controlla nulla.
5. **Eval.** Lo squat lo trova solo `held()` (`src/trainer/adapt_evaluation.py:328-338`): `Front_Barbell_Squat` ha `movement_pattern = squat`, che è in `without_pattern`, quindi `LEFT_OUT`.

**Cosa ha fatto il modello**

Ha preso il workout del giorno, che conteneva un back squat, e ha tolto *quell'*esercizio mettendo al suo posto il parente più vicino: «front squat replaces back squat». È una lettura possibile della frase, solo diversa da quella della riga. Nelle altre 2 ripetizioni su 3 l'ha letta come pattern. Il record della run fallita non l'ho trovato in locale, quindi la ricostruzione si basa sulla riga del ticket e sul codice, non sull'output grezzo.

**Il precedente**

Nel primo pass lo stesso errore aveva un'altra causa: *«`Dumbbell_Squat` kept: `leave_out` takes ids, «niente squat» is a pattern»*. Lì il canale strutturato c'era, ma accettava solo id. Dopo `1057b2a` («the planner reads the words») è rimasto solo `said`, e la decisione è passata tutta al modello.

**Dove sta la linea**

La charter del planner (`evals/planner/charter.md:19`) lascia **libero** il modello di decidere, in un adattamento, «an exercise in or out, read off what the user said». Ci sono due strade:

- **Senza spostare la linea:** aggiungere al prompt di `adapted` un criterio come *«un movimento nominato in modo generico ("niente squat", "niente stacchi") è tutto il pattern, non l'esercizio del giorno»*. Guida il giudizio senza dettare la risposta, quindi resta nella charter. Va misurato, e quindi costa.
- **Spostando la linea:** far compilare all'entrance `exclude` (che `adaptation_requested` già accetta e classifica come pattern) e filtrare l'insieme ammissibile nel codice. Così lo squat non sarebbe più possibile, ma la scelta «quale esercizio fuori» passerebbe dal modello al codice. La decisione spetta a te.

C'è anche un'incoerenza nel set. «Held» ha una soglia del 100% su ciò che il codice garantisce, ma `without_pattern` oggi non lo garantisce nessun codice: misura un giudizio del modello. Finché la linea resta dov'è, questa riga non può reggere il 100% per costruzione. O la si conta a parte, o si sposta la linea.