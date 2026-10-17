## Il primo errore: «niente squat» → `Front_Barbell_Squat`

**Il planner legge testo libero. Non c'è nessuna regola che toglie un solo esercizio, e nemmeno una che toglie lo squat.**

### Il percorso della frase

1. **Entrance → planner.** `adapt_this_workout(said)` passa al planner solo le parole dell'utente, così come le ha scritte (`src/trainer/coach/entrance.py:70`). `requested()` chiama `adaptation_requested(connection, today, said=said)` con un `Asked()` vuoto (`entrance.py:776`). Quindi non passa nessun `exclude`, nessun `avoid`, nessun `named`.
2. **La richiesta.** `adaptation_requested` (`src/trainer/plan.py:525`) usa come insieme ammissibile **tutto il catalogo**, tolte solo le esclusioni già attive nel database. Siccome `asked` è vuoto, anche `named` è vuoto (`plan.py:574-579`). Gli squat restano tutti ammissibili.
3. **Il brief.** `adapted()` (`src/trainer/coach/planner.py:255`) mette «oggi niente squat, proponi tu» in cima, come «the first thing it answers to», e subito dopo l'intero mesociclo con il workout di oggi, dicendo «start from it unless what they said points elsewhere».
4. **Il validatore.** Su un adattamento controlla solo: nessun esercizio doppio, id ammissibile, preferenze dichiarate, piano non già rifiutato, `counts_as` (`plan.py:830-856`). Il commento alla riga 838 lo dice chiaro: *«An adaptation answers to what the user said, which no rule reads»*.

### Perché è uscito il front squat

Il modello è Haiku 4.5. Ha letto «niente squat» come «niente *quello* squat», cioè il back squat del workout di partenza, e l'ha sostituito con una sua variante. Il front squat però ha lo stesso `movement_pattern`. L'eval controlla il pattern, non l'id (`src/trainer/adapt_evaluation.py:333`), quindi il caso fallisce. Nelle altre 2 ripetizioni su 3 il modello ha letto la frase come il pattern intero.

C'è un'ipotesi che non ho verificato sul transcript del run: il brief parla di «an exercise in or out» e dice di partire dal workout del giorno. Questa formulazione spinge a pensare per sostituzioni di esercizi, non di pattern. E «proponi tu» invita a sostituire.

### Cosa dice il charter

`evals/planner/charter.md:20`: in un adattamento, *quali esercizi entrano o escono* è una decisione **libera** del planner, perché nessuna regola del validatore legge le parole (ADR-0008 item 6). Quindi l'errore è un'interpretazione sbagliata del modello, non un bug nel codice.

### Le due strade

- **Restando dentro il charter.** Si aggiunge al brief di `adapted()` un criterio di lettura, per esempio: un movimento nominato in modo generico («squat», «stacchi», «panca») esclude tutto il pattern, non solo l'esercizio del workout di partenza. È un criterio che informa il giudizio, non detta la risposta, quindi la linea non si sposta. Per vedere se funziona serve un nuovo passaggio di eval, che costa (il passaggio di chiusura è costato $1.22).
- **Spostando la linea.** L'entrance o il codice traducono «niente squat» in un `asked.exclude`, che il motore filtra dall'insieme ammissibile. Il risultato diventa garantito invece che probabile, ma la scelta di cosa esce passa dal planner al codice. Inoltre si usa per una scelta del giorno un meccanismo che il charter riserva alla sicurezza (riga 25: «Exclusions … are safety, not preference»). Questa decisione spetta a te, e non l'ho toccata.

Se vuoi provare la prima strada, preparo la modifica al prompt e i controlli locali gratuiti. Poi ti chiedo l'approvazione per il passaggio di eval, con il costo stimato.