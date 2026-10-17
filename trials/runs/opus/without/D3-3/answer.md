Ho tolto le regole invece di aggiungerne una. Un adattamento ora è vincolato solo da ciò che è legale, e il gruppo dello slot non lo limita più. **Non ho però potuto lanciare né i test né mypy**: l'esecuzione di `pytest` richiedeva un'approvazione che questa sessione non può dare, ed è stata bloccata. Quindi la modifica non è verificata.

## Dov'era il vicolo cieco

Lo slot 1 della fixture è `legs, core`. L'adattamento era legato ai gruppi dello slot in tre punti:
- l'insieme ammissibile veniva ristretto ai gruppi dello slot;
- `every_group_trained` pretendeva che ogni gruppo fosse allenato;
- un esercizio chiesto fuori da quei gruppi veniva rifiutato, col suggerimento di "passare `workout`".

Con «oggi faccio il core ma niente gambe», lo slot 1 obbligava a fare le gambe e gli slot 2 e 3 non contengono il core. Non esisteva nessun piano legale.

## Cosa ho cambiato

- **Codice** (`src/trainer/plan.py`, `adaptation_requested`): la richiesta di un adattamento non ha più gruppi né allocazione. Restano i vincoli legali: esclusioni, attrezzatura di oggi, minuti, esercizi chiesti ed esclusi. Lo slot resta il punto di partenza e indica quale allenamento del ciclo viene contato come fatto. Il suggerimento "passa `workout`" è stato tolto.
- **Brief del planner**: ora dice esplicitamente che la richiesta dell'utente viene prima. Se contraddice lo slot (altri gruppi, meno gruppi, di più), il planner segue la richiesta.
- **Tool dell'entrance**: la descrizione di `workout` dice che è la richiesta a decidere cosa si allena, non il numero. «oggi solo core» non ha bisogno di un numero.
- **CLI**: `trainer plan --time 30` non stampa più `-- legs` dopo "adapting mesocycle workout …", perché quella riga ora sarebbe falsa.
- **Test**:
  - aggiornati i quattro che controllavano i gruppi di un adattamento;
  - il test "panca militare nel giorno gambe rifiutata" è diventato il test di regressione: un piano di sole spalle nel giorno gambe deve passare la validazione senza violazioni.
- **Documenti**:
  - nuova ADR-0014 (*An adaptation is held to what is legal, not to its slot*), che modifica il punto 6 dell'ADR-0008;
  - aggiornate le voci Adaptation e Admissible set in CONTEXT.md, la spec della sessione 14 e il ticket 04;
  - aggiunta la riga `core-only` al set di adattamento, che controlla che il piano non alleni le gambe.

## Una conseguenza

Se l'utente allena solo il core al posto dello slot gambe, quello slot viene contato come fatto anche se le gambe non sono state allenate. È coerente con «prima la volontà dell'utente», e il deficit di volume lo mostrerà. Se preferisci un comportamento diverso, va deciso nell'ADR.

## Cosa serve da te

1. **Test e mypy**: lanciali tu, oppure abilita l'esecuzione e li lancio io:
   `uv run pytest -q` e `uv run mypy src`
2. **Eval** (consuma crediti, quindi aspetto il tuo via): `trainer eval --suite adapt`, con il `TRAINER_DB` della fixture.
   - **Costo**: il secondo passaggio, con le scelte dell'ADR-0011, è costato $0.44 per 19 righe. Con 20 righe stimo circa $0.45–0.50.
   - **Tempo**: circa 23 secondi per esecuzione.
   - Mi aspetto che `pull-ups`, `football` e `core-only` non finiscano più rifiutati.

Qui non c'è un repository git, quindi non ho fatto nessun commit.