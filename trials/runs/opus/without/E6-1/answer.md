Il planner legge testo libero. Non c'è nessuna regola, né una che toglie un solo esercizio né una che toglie tutti gli squat. Il miss di `you-choose` è una scelta del modello del planner.

**Il percorso di «oggi niente squat, proponi tu»**

1. **Entrance.** Il modello chiama `adapt_this_workout(said="oggi niente squat, proponi tu")`. Il tool ha un solo argomento, la frase dell'utente.
2. **Costruzione della richiesta.** `entrance.requested` (`src/trainer/coach/entrance.py:768`) chiama `plans.adaptation_requested(connection, today, said=said)` senza passare un `Asked`. Quindi `asked.exclude` è vuoto. Le esclusioni della richiesta sono solo quelle già salvate nel DB (`constraints.constraining_today`). Dalla frase non viene fuori nessuna esclusione strutturata (`src/trainer/plan.py:550-555`).
3. **Prompt del planner.** `planner.adapted` (`src/trainer/coach/planner.py:255`) mette la frase così com'è sotto *"what they said is the first thing it answers to"*. Poi aggiunge un'istruzione generica: *"an exercise in or out … Where they leave something to you, decide it"*. Il prompt spiega esplicitamente solo l'attrezzatura («solo kettlebell» vuol dire che ogni esercizio usa la kettlebell). Per «niente X» non c'è un'istruzione equivalente.
4. **Validator.** Per un'adattamento `validate` (`src/trainer/plan.py:837-839`) salta budget e gruppi: *"An adaptation answers to what the user said, which no rule reads"*. Restano duplicati, ammissibilità, preferenze, piani già rifiutati e `counts_as`. Nessuna di queste regole guarda il movement pattern rispetto alla frase. Il `Front_Barbell_Squat` è passato perché era ammissibile.

**Perché ha sbagliato**

Il modello ha letto «niente squat» come «niente *back* squat» e l'ha sostituito con il front squat, scrivendo nel `reason` «front squat replaces back squat». Nessuno strato lo poteva fermare:
- il prompt non dice che «niente squat» indica il pattern;
- la richiesta non contiene un'esclusione;
- il validator non legge la frase.

L'ha preso solo lo scorer dell'eval: `adapt_evaluation.py:333` controlla `movement_pattern in case.without_pattern`.

La lettura giusta non è ovvia, e il set lo mostra. La riga subito sopra (`eval-set.toml:74-77`) dice «oggi niente squat, … bulgari» e *pretende* uno split squat o un affondo. Quindi «squat» vuol dire il pattern `squat` del catalogo, non ogni esercizio che ha "squat" nel nome. Il criterio esiste solo nello scorer, nel prompt non c'è. 1 su 3 è il tasso con cui il modello indovina da solo.

**Due possibili correzioni, da decidere**

- **Prompt:** una riga in `adapted()` che dica che «niente <pattern>» toglie l'intero movement pattern del catalogo. È economica, ma resta probabilistica.
- **Struttura:** l'entrance passa anche le esclusioni di oggi (per esempio un argomento `exclude` classificato con `exclusion_state.classify`). Così `_every_id_admissible` rifiuta il front squat in modo deterministico. È più solida, ma cambia la firma del tool e il routing, quindi va rimisurata.

Consiglio la seconda, perché sposta il vincolo nel validator, dove per ADR-0001 stanno le regole. Rimisurarla però vuol dire rifare il pass sui modelli. L'ultimo è costato $1.22 per 3 ripetizioni su tutto il set, e lo lancio solo con la tua approvazione.