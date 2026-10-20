Ho letto il codice: come arriva la frase dell'utente al planner e cosa controlla il validator. Ecco la risposta.

---

**Il planner riceve solo testo libero, e nessuna regola tiene fuori lo squat.** Il front squat non l'ha tolto il codice: l'ha scelto il modello, leggendo male la frase dell'utente.

### Il percorso di «oggi niente squat, proponi tu»

1. **Entrance**: `adapt_this_workout(said: str)` (`src/trainer/coach/entrance.py:70`) ha un solo argomento. Il modello lo chiama con le parole dell'utente.
2. **Richiesta**: `entrance.requested` (`entrance.py:768`) prende solo `said` e chiama `plans.adaptation_requested(connection, today, said=said)` con un `Asked()` vuoto.
3. **Esclusioni**: in `adaptation_requested` (`src/trainer/plan.py:523`) le esclusioni di oggi vengono solo da `asked.exclude`, che dalla chat è sempre vuoto. Restano quindi le esclusioni già salvate e nessuna per «squat». L'attrezzatura è tutta quella del catalogo, quindi anche il set ammissibile è il catalogo intero.
4. **Prompt**: `planner.adapted` (`src/trainer/coach/planner.py:255`) scrive la frase così com'è, come «the first thing it answers to», e aggiunge «an exercise in or out… Where they leave something to you, decide it». La riga `They also named, and the plan keeps to it: no squat` uscirebbe solo se `asked.exclude` fosse pieno, e dalla chat non lo è mai.
5. **Validator**: con `adapting` impostato, `validate` (`plan.py:837`) salta di proposito budget e gruppi («An adaptation answers to what the user said, which no rule reads»). Restano duplicati, ammissibilità, preferenze, piani già rifiutati e `counts_as`. Nessuna di queste guarda il pattern di movimento.

### Allora perché è sbagliato in 1 caso su 3

Al modello arrivano solo le parole, e in un caso su tre ha letto «niente squat» come «niente back squat». Ha sostituito l'esercizio dentro lo stesso pattern invece di togliere il pattern. «Proponi tu» lascia ancora più spazio, e il prompt lo rafforza con «decide it». Tutto il codice a valle accetta il piano, perché `Front_Barbell_Squat` è ammissibile. Solo l'eval lo segna come errore, con il controllo `without_pattern` (`src/trainer/adapt_evaluation.py:333`).

### Cosa consiglio

Il motore ha già il meccanismo giusto: `Asked.exclude`, cioè pattern o articolazioni nel vocabolario del catalogo, validi per un solo piano. Da lì passa per `classify`, poi `constraining_today`, poi il set ammissibile. Il terminale lo usa già con `--exclude`. Manca solo il collegamento dalla chat:

- dare a `adapt_this_workout` un argomento `exclude`, oltre a `said`;
- farlo leggere a `entrance.requested` e passarlo in `Asked(exclude=...)`.

A quel punto «niente squat» diventa un vincolo: il front squat non è più nel set ammissibile, e il planner legge anche «They also named… no squat». Il rischio si sposta sull'entrance, che deve tradurre «squat» nel valore del catalogo. Però `classify` rifiuta un valore sconosciuto e lo dice, invece di lasciarlo passare in silenzio.

Non ho cambiato niente. La verifica richiede un nuovo passaggio dell'eval su `you-choose`, che consuma crediti. Prima di lanciarlo ti chiederei l'ok con una stima: il passaggio completo è costato $1.22, una sola riga costa molto meno.