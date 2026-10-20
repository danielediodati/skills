---

# ⚠️ Ticket 10.3 — costruito, non chiuso
### Il bot distingue un cambio da un adattamento e li porta fino al database
nessun commit (la cartella non è un repo git) · 1549 test · mypy pulito · niente rotto

---

**Cosa è stato costruito**
L'entrance ha due nuovi handoff senza argomenti, `adapt_today` e `change_mesocycle`. Il planner riceve le parole dell'utente così come le ha scritte. Per un adattamento parte dallo slot di oggi; accettato, diventa il servito di oggi e il mesociclo resta com'era. Per un cambio parte dal mesociclo attivo; accettato, lo sostituisce e il conteggio dei cicli prosegue. Anche `trainer plan --time/--equipment/--exclude/--avoid` ora adatta lo slot di oggi quando c'è un mesociclo.

**Cosa puoi lanciare**
```
$ uv run pytest -q
........................................................................ [  4%]
...
.....................................                                    [100%]
$ uv run mypy
Success: no issues found in 85 source files
```
Non ho lanciato `trainer plan --time 30` né il bot su un modello vero, vedi sotto.

**Cosa si è rotto rispetto a prima**
Niente. Prima di iniziare 3 test di `test_bot.py` fallivano già: la data di retest della fixture (`2026-10-15`) è passata, e il logger la rifiuta giustamente. Li ho agganciati a oggi + 30 giorni.

**Dove siamo**
1549 test verdi, mypy pulito. I criteri 1–3 sono verificati solo con un modello scriptato. Il percorso dal handoff al database l'ho visto funzionare. La lettura del modello non l'ho vista: non c'è `.env` e la chiamata a `ollama` mi è stata bloccata. Per verificarla serve una prova su `llama3.1` locale, oppure, se va su Groq, un budget da concordare.

**Il confine che non ho spostato.** In chat, il vincolo di oggi (*"solo 30 minuti"*, *"niente manubri"*) arriva al planner solo come parole. Il validatore controlla ancora il cap dichiarato e l'attrezzatura dichiarata. Si può renderlo vincolante in due modi, e ciascuno sposta un confine:
- un argomento sull'handoff (charter dell'entrance: *gli handoff non prendono argomenti*);
- un `Request` ricavato dalle parole prima della run (charter del planner: *il request è assemblato prima di qualsiasi chiamata al modello*).

Il bottone *Solo 30 minuti* sulla proposta adattata invece vincola davvero. La decisione è tua.

**Decisioni da rivedere**
- **Charter dell'entrance non aggiornato.** Il testo elenca ancora tre handoff e dice che solo `plan_mesocycle`/`log_workout` portano avanti la run. Il confine è lo stesso (insieme chiuso, senza argomenti), ma il testo va aggiornato da te.
- **Il servito di oggi viene cancellato.** Un adattamento o un cambio cancella il servito di oggi se nessuno l'ha eseguito. Altrimenti resterebbero due prescrizioni aperte per lo stesso slot e il volume deficit verrebbe falsato. Questo va contro lo spirito del "niente upsert" di `record_prescribed`.
- **Come conto i cicli di un cambio.** Il `cycles` del modello conta dal ciclo in corso; nel database salvo cicli già fatti + quel numero. Nella proposta compare "N cicli da adesso", mentre il servito mostra "ciclo c di totale".

**Passi di chiusura non fatti**
- `/code-review` non è disponibile qui come strumento. Ho rivisto il diff io: i punti sopra vengono da lì.
- Senza git non c'è un hash, quindi non ho segnato il ticket done in ROADMAP. Non ho nemmeno cancellato il file del ticket: senza storia, quello che contiene andrebbe perso.
- Quello che serve al ticket 04 l'ho scritto nella sua sezione *Left by 03*. Il README ora descrive la chat e `plan --time 30`.