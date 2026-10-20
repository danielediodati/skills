Il planner legge testo libero. Non c'è nessuna regola che toglie un solo esercizio, e nemmeno una che toglie tutto il pattern squat. In 1 run su 3 il modello del planner ha letto «niente squat» come «niente `Barbell_Squat`», e nessun controllo nel codice l'ha fermato.

**Il percorso della frase**

1. **Entrance.** `adapt_this_workout(said)` riceve solo la frase (`src/trainer/coach/entrance.py:70`). Dalla 14.4 i campi `ask_for`, `workout`, `equipment` ed `exclude` non ci sono più, quindi nulla di «niente squat» diventa un vincolo strutturato.
2. **Request.** `adaptation_requested` (`src/trainer/plan.py:523`) costruisce la richiesta su tutto il catalogo, togliendo solo le esclusioni salvate nel DB. `Asked()` è vuoto, quindi `exclude=()` e `named=()`. `Front_Barbell_Squat` resta nel set ammissibile.
3. **Brief.** `adapted()` (`src/trainer/coach/planner.py:255`) mette la frase in cima, così com'è: «what they said is the first thing it answers to». È l'unico punto in cui «squat» arriva al planner.
4. **Validator.** In un adattamento controlla duplicati, ammissibilità, preferenze, rifiuti e `counts_as`, ma non tempo e gruppi (`plan.py:837`). Nessun controllo legge la frase. Lo dice anche l'eval set (`docs/adapting/eval-set.toml:17`): «The validator holds none of these … only the set can». Per questo l'errore si vede solo nell'eval: `held()` trova `movement_pattern = "squat"` su `Front_Barbell_Squat`.

**Perché proprio quella lettura (ipotesi, non verificata)**

Il brief dice «start from workout 1» e mostra la sessione gambe con `Barbell_Squat` come primo blocco. Elenca anche «an exercise in or out» tra le modifiche tipiche. Con questi ancoraggi, sostituire lo squat con la variante più vicina è una lettura plausibile per Haiku. La nota del planner, «front squat replaces back squat», dice proprio questo: ha tolto un esercizio, non il movimento. Non ho il run record, quindi non ho verificato se l'entrance abbia passato `said` parola per parola o l'abbia riformulato. È la prima cosa da guardare.

**Cosa si può fare, e cosa non tocca a me**

- **Un criterio nel brief, senza spostare linee.** Per esempio: «un movimento nominato in generale ("niente squat", "niente stacchi") vale per tutto il pattern, non per l'esercizio della scheda». Informa il giudizio del modello e non decide al suo posto, quindi è ammesso dal charter (`evals/planner/charter.md:19`: nell'adattamento «the user's words bind it»).
- **Un vincolo in codice: è una linea, la decisione è tua.** Si tratta di rimettere un campo `exclude` sull'handoff, oppure di estrarre il pattern dalla frase. In cambio, «niente squat» diventerebbe un'esclusione garantita al 100% dal validator, invece che affidata alla lettura del modello. Però riporterebbe in codice ciò che la 14.4 e ADR-0008 item 6 hanno lasciato al planner, e ricreerebbe il problema di `hinge-excluded`: campi compilati male o non compilati affatto.

Un controllo del criterio costa una ripetizione di `you-choose`: circa $0.02 secondo il passaggio del 3 ottobre ($1.22 per 57 run). Non lo lancio senza il tuo ok.