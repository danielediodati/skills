---

# ⚠️ Ticket 10.3 — non chiuso
### Adattamento e modifica sono scritti, ma niente è stato eseguito
nessun commit · test non eseguiti · mypy non eseguito · regressioni non verificate

---

**Perché non è chiuso.** In questa sessione ogni comando Python (`pytest`, `mypy`) richiedeva un'approvazione che qui non poteva arrivare, quindi è stato bloccato. Anche la chiamata a Ollama per avere un modello vero è stata bloccata. La cartella poi non è un repository git, quindi niente commit né hash. Per CLAUDE.md un ticket non si chiude senza criteri verificati, suite verde e `/code-review`: non ho segnato niente come fatto in ROADMAP.md e il file del ticket resta, con `Status: ready-for-human` e la lista di cosa manca.

## Cosa è stato costruito
- **Adattamento** (`adapt_today`): il planner parte dallo slot di oggi del mesociclo e riceve le parole dell'utente così come sono state scritte. Il modello dichiara cosa ha capito del vincolo: `minutes` (i minuti disponibili oggi) e `without` (l'attrezzatura che oggi manca, scelta tra quella dichiarata). Il validatore controlla il workout contro la richiesta ristretta da quei valori, e un valore dichiarato può solo stringere la richiesta, mai allargarla. Una volta accettato, il workout diventa il servizio dello slot di oggi nella tabella `served` (`record_adapted`), e il mesociclo resta com'era.
- **Modifica** (`change_mesocycle`): il planner riceve il mesociclo attivo e le parole dell'utente. Una nuova regola, `cycles`, rifiuta una proposta che cambia il numero di cicli. Una volta accettata, `record_mesocycle(continuing=…)` sostituisce il mesociclo e conserva `accepted_after`, quindi il conteggio dei cicli continua.
- **L'entrance distingue i due casi**: il prompt dice di chiedere quando non si capisce se vale solo per oggi o da ora in poi. Al pianificatore arrivano gli ultimi due messaggi dell'utente, cioè la richiesta e la risposta alla domanda. Senza un mesociclo il pianificatore non parte, e l'entrance dice che manca.
- **CLI**: con un mesociclo attivo, `--time`, `--equipment`, `--exclude` e `--avoid` adattano il workout di oggi. `--workout` e `--group` pianificano ancora da zero.

## Cosa puoi lanciare
Niente di verificato. Da lanciare per primi:
```
uv run pytest
uv run mypy
uv run trainer plan --time 30
```
Ho aggiunto 25 casi di test (planner, entrance, bot, CLI). Usano modelli simulati, quindi provano il collegamento tra i pezzi ma non la lettura del modello. Il criterio 3 (*una frase ambigua porta a una domanda*) si può verificare solo con un modello vero.

## Cosa si è rotto rispetto a prima
Non lo so: la suite non è stata lanciata.

## Dove siamo
- Test e mypy: non eseguiti.
- `/code-review`: non eseguito. Ho riletto il codice a mano e ho trovato e corretto due problemi:
  - quando lo slot era già stato servito, `record_served` restituiva i blocchi del mesociclo e non quelli del workout prescritto, quindi un adattamento sarebbe stato servito come lo slot originale;
  - l'intestazione dell'adattamento mostrava i minuti letti dal modello e non quelli contro cui il workout è stato controllato.

Quando il ticket 10.3 sarà chiuso si sbloccano 10.4 e 10.5.

**Una decisione è tua.** Se un adattamento viene accettato dopo che lo slot era già stato servito, la prescrizione originale resta nella tabella `workouts`. Prima o poi comparirà tra gli allenamenti non riportati. L'ho lasciata così perché cancellare dati di allenamento non si annulla, e il codice esistente tiene sempre separate due prescrizioni diverse. Se preferisci eliminarla, la modifica va in `record_adapted`.