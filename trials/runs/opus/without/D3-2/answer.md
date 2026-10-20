Ho tolto la regola che bloccava «oggi faccio il core ma niente gambe», ma **non ho potuto eseguire né i test né mypy**: in questa sessione ogni comando che richiede approvazione viene rifiutato in automatico. Va fatto girare tutto prima di considerare la modifica buona.

### Dov'era il vicolo cieco
In un adattamento il codice imponeva i gruppi della seduta in programma: nella fixture la seduta 1 è `legs, core`. Ogni strada per dire «core sì, gambe no» era chiusa:
- **Il campo `groups`:** veniva rifiutato.
- **Il validatore:** pretendeva un esercizio per le gambe.
- **Un'altra seduta del ciclo:** nessuna è «solo core».

Aggiungere un'altra regola avrebbe solo spostato il problema. Quindi ho tolto quella che c'era.

### Cosa è cambiato
- **I gruppi della seduta non sono più un vincolo** (`plan.py`, `adaptation_requested`). Restano nell'adattamento in un nuovo campo `Adapting.groups`, ma solo come punto di partenza. La richiesta adesso non porta gruppi, quindi il validatore non controlla quali gruppi si allenano e gli esercizi ammessi sono tutto il catalogo.
- **Il codice controlla ancora:** esclusioni, attrezzatura, minuti, esercizi chiesti ed esercizi lasciati fuori. Cioè le regole di sicurezza e quello che l'utente ha detto esplicitamente.
- **Le istruzioni al planner** (`planner.py`, `adapted`) ora dicono che la seduta del ciclo è un punto di partenza e che *«What they said comes first»*: se le parole dell'utente non coincidono con la seduta, si pianifica quello che ha detto, gruppi compresi.
- **Non c'è più il rifiuto per gruppo:** chiedere le trazioni (o un press) nel giorno gambe adesso viene pianificato. Il rifiuto per esclusione con la data di re-test resta.
- **La CLI** stampa i gruppi della seduta da `adapting.groups`.

### Test (scritti, non eseguiti)
- `test_plan.py`: le asserzioni sui gruppi ora si aspettano `()` nella richiesta e i gruppi della seduta in `adapting.groups`. Il test «press nel giorno gambe rifiutato» ora verifica che venga pianificato. Ne ho aggiunti due:
  - un esercizio chiesto senza l'attrezzatura che serve viene ancora rifiutato;
  - una seduta di solo core nel giorno gambe non riceve né `UNTRAINED` né `ADMISSIBLE`.
- `test_adapt_this_workout.py`: aggiornati i casi 0 e 2, più un caso nuovo «core ma niente gambe».
- `test_planner.py`: il brief contiene *«What they said comes first»* e non più *«This workout trains»*.

### Documenti
- **Set di valutazione:** nuovo caso `core-no-legs` in `docs/adapting/eval-set.toml` (deve finire su `adapt_this_workout`, e il piano non deve allenare le gambe).
- **Spec:** nuova riga *What this workout trains* in `spec.md`.
- **ADR-0008, punto 6:** la seduta da cui parte un adattamento è un punto di partenza, e le parole dell'utente vincono.
- **Ticket 04:** tolta la nota sul rifiuto della riga 8 (le trazioni).

### Cosa resta da fare
1. Lanciare `pytest` e `mypy` e dirmi il risultato.
2. La cartella non è un repository git, quindi non ho fatto commit.
3. Per vedere l'effetto sul modello bisogna rifare il passaggio `trainer eval --suite adapt`, che costa crediti. L'ultimo è costato $0.44; con un caso in più la stima è circa $0.45–0.50 a ripetizione. Lo lancio solo se mi dai il via.