# Ticket 10.3: non è chiuso

Ho costruito la parte che si poteva fare senza toccare i charter. Però **non ho eseguito niente**: il permesso di lanciare test e mypy è stato negato, e la cartella non è un repository git, quindi niente commit (anche se il ticket cita `674648c`). Nessun criterio è spuntato e ROADMAP non è segnata.

## Una decisione tua: l'adaptation dalla chat sposta una linea

Perché *"solo 30 minuti oggi"* funzioni, i 30 minuti devono entrare nella `Request`. Se restano solo nel brief, il validator controlla il piano contro i minuti dichiarati (45) mentre il modello legge 30. È proprio il caso che il charter del planner vieta: un vincolo applicato da un lato solo. Ogni strada che porta i minuti nella `Request` sposta una linea:

| Opzione | Linea spostata |
|---|---|
| **`adapt_today(minutes, equipment, exclude)`**: l'entrance traduce le parole in campi di `Asked`, che `plans.requested` controlla come i flag della CLI (cap, vocabolario letto dai dati). **La consiglio.** | entrance: *"Handoffs take no arguments"* |
| Il planner fissa da solo minuti e attrezzatura | planner: *"What the plan is made against is never in the plan"* |
| Le parole restano solo nel brief | planner: *"Today's constraints are folded into a single-workout request once"* |

La prima opzione è l'unica in cui il piano adattato viene davvero verificato contro i 30 minuti richiesti. Finché non decidi, il prompt dell'entrance dice che un vincolo valido solo per oggi non si può ancora pianificare dalla chat. Ho scritto la decisione nel ticket e l'ho messo `Status: needs-info`.

## Cosa è stato costruito (non verificato)

- **Change.** C'è un nuovo handoff `change_mesocycle`, senza argomenti. Il planner riceve il mesociclo attivo e le parole dell'utente così come sono state scritte. Se l'entrance ha chiesto *«solo oggi o da ora in poi?»*, arrivano entrambi i messaggi, cioè tutto quello che l'utente ha scritto dall'ultimo handoff. Una volta accettato, il nuovo mesociclo sostituisce il vecchio e continua il conteggio dei cicli. Il numero di cicli lo sceglie ancora il modello, contati da quello in corso. Se non c'è un mesociclo attivo, diventa un mesociclo nuovo.
- **Adaptation.** Il planner in modalità singolo allenamento riceve lo slot di oggi come punto di partenza. Una volta accettato, diventa la serving dello slot nella tabella `served` e sostituisce quella vecchia; il mesociclo non cambia. Dalla CLI si raggiunge con `trainer plan --time 30` (o `--equipment`, `--exclude`, `--avoid`) quando un mesociclo è attivo; con `--workout` o `--group` si pianifica ancora da zero.
- **Test scritti ma mai eseguiti** in `test_mesocycles`, `test_planner`, `test_entrance`, `test_bot` e `test_cli`. Ho anche aggiunto `Adapting` e `Change` a `checkpoints.DECLARED`, altrimenti un piano in attesa non si rileggerebbe dal checkpoint.

## Cosa resta

- **Il charter dell'entrance è da aggiornare, ma solo da te.** Dice *«three handoffs»* e ora sono quattro. A mio giudizio aggiungere un handoff non sposta una linea: la lista resta chiusa in codice e la scelta resta al modello. Il testo del charter però adesso è inesatto.
- **Test e mypy da lanciare**: `uv run pytest` e il type check.
- **Criteri di accettazione 1–3**: servono un modello vero sull'entrance, quindi una run da approvare, con un budget da concordare. Non ho speso niente.