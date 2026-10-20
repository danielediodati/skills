Ho letto il codice. Ecco la risposta.

**Il planner legge testo libero. Non esiste nessuna regola che tolga qualcosa, né un esercizio solo né un pattern.**

Il percorso dalla chat:

1. `adapt_this_workout(said: str)` (`src/trainer/coach/entrance.py:70`) ha un solo argomento, le parole dell'utente.
2. `entrance.requested` (`entrance.py:768`) chiama `plans.adaptation_requested(connection, today, said=said)` e lascia `asked` vuoto (`Asked()`). `asked.exclude` quindi resta vuoto, e le uniche esclusioni nella `Request` sono quelle già attive nel DB (`plan.py:550-559`).
3. `said` finisce in `Adapting.said`. `planner.adapted()` (`src/trainer/coach/planner.py:255`) lo scrive nel prompt come «what they said is the first thing it answers to», seguito da «Read what they said and plan the workout it asks for -- … an exercise in or out». Il modello quindi interpreta «niente squat» da solo.
4. Il validatore non lo controlla. In `validate` (`plan.py:837-839`), per un adattamento vengono saltati budget e gruppi, con il commento esplicito *«An adaptation answers to what the user said, which no rule reads»*. Restano solo duplicati, ammissibilità, preferenze, piani già rifiutati e `counts_as`. `Front_Barbell_Squat` è ammissibile e passa.

Il miss quindi non viene da un bug di una regola. È il modello che ha capito «niente squat» come «niente back squat»: ha tolto l'esercizio e ha messo un altro squat. L'eval invece controlla il pattern (`adapt_evaluation.py:333`, `movement_pattern in case.without_pattern`) e boccia il piano.

**La strada deterministica c'è già, ma la chat non la usa.** `Asked.exclude` passa da `exclusion_state.classify` e da `constraining_today`, e così toglie il pattern dall'insieme ammissibile. La porta della CLI lo riempie con i suoi flag. La porta della chat no, perché il tool riceve solo `said`.

Le correzioni possibili, dalla più leggera:

| opzione | cosa cambia | costo |
|---|---|---|
| una riga in `adapted()`: «"niente X" su un pattern toglie ogni esercizio di quel pattern» | solo il prompt | resta probabilistico |
| `adapt_this_workout` riceve anche `exclude: list[str]`, l'entrance lo riempie e finisce in `asked.exclude` | l'esclusione diventa vincolante e il validatore la fa rispettare | cambia la firma del tool e il routing. Bisogna verificare che `constraining_today` la tenga solo per oggi e non la renda permanente: non l'ho controllato |

Io sceglierei la seconda. È coerente con `named` («binding, unlike the words», `plan.py:283`): quello che si può nominare come pattern lo nomina l'entrance, e il resto lo legge il planner. Tocca però una scelta di ADR-0011 sulla firma dei tool, quindi va deciso lì prima di scrivere codice.

Non ho rilanciato nessuna eval. Questa spiegazione viene dal codice e dalla riga del ticket, non da un record della run: il record di `you-choose-*-plan` non l'ho aperto.