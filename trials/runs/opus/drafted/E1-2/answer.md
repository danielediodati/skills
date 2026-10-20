---

# ⏸️ Ticket 10.3 — non chiuso, fermo su una riga del charter
### Il motore, il planner e la CLI sanno fare un adattamento e una modifica; la chat no
nessun commit (la cartella non è un repo git) · 1541 test · mypy pulito · niente rotto

---

**Cosa è stato costruito**
- **Adattamento.** Il planner, in modalità singolo allenamento, riceve nel brief lo slot di oggi del mesociclo come punto di partenza. Se lo accetti, l'allenamento adattato diventa quello servito per lo slot di oggi (tabella `served`) e prende il posto di un eventuale servito precedente. Il mesociclo resta com'è.
- **Modifica.** Il planner, in modalità mesociclo, riceve nel brief il mesociclo attivo e il ciclo in cui sei. Se lo accetti, il nuovo mesociclo sostituisce il vecchio e il conteggio dei cicli continua. Il numero di cicli resta una scelta del modello, contato dal ciclo in corso.
- **CLI.**
  - `trainer plan --time 30` (e anche `--equipment`, `--exclude`, `--avoid`) adatta lo slot di oggi quando c'è un mesociclo attivo.
  - `trainer plan --change ...` riscrive il mesociclo attivo.
  - Con `--workout` o `--group` il piano si fa da zero, come prima: quelle opzioni chiedono un altro allenamento, non quello di oggi.

**Cosa puoi lanciare**
Niente che abbia girato davvero: la `.env` non c'è, quindi non ho chiamato nessun modello e non ho niente da incollare. I comandi sopra sono coperti da test con un modello finto (5 test CLI, 6 del motore, 5 del planner).

**Criteri di accettazione**
- I primi tre (*«solo 30 minuti oggi»*, *«basta affondi»*, la frase ambigua) non sono soddisfatti: passano tutti dall'entrance, che non ho toccato. Il motivo è sotto.
- Suite e mypy sono verdi.

**Cosa si è rotto rispetto a prima**
Niente di questo ticket. C'erano però 3 test di `test_bot.py` già rossi prima che toccassi qualcosa: la data di re-test nel fixture era fissa al `2026-10-15`, che ormai è passata. Ora la data del fixture è calcolata rispetto a oggi.

**Dove siamo: serve una tua decisione sul charter dell'entrance**
Per portare il ticket in chat bisognerebbe spostare due righe di `evals/entrance/charter.md`:
1. **La lista degli handoff** è chiusa e nominata: `todays_workout`, `plan_mesocycle`, `log_workout`, senza argomenti. Per distinguere modifica e adattamento servono due handoff in più, per esempio `adapt_today` e `change_mesocycle`.
2. **Il vincolo dell'adattamento.** «30 minuti» o «niente manubri» deve arrivare in `budget_min` ed `equipment` della richiesta. Altrimenti il validatore controlla i limiti dello slot e non quelli di oggi. Senza argomenti e senza regole a parole chiave, l'unico modo è che il modello del planner legga le tue parole. Così però il controllo di budget e ammissibilità passerebbe dal codice al modello.

   Le alternative:
   - l'handoff riceve `minutes` ed `equipment` come argomenti: sposta la riga *«take no arguments»*;
   - un nuovo passaggio stocastico che estrae il vincolo: va scritto prima un charter tutto suo.

   Con una di queste due, il vincolo resterebbe controllato dal codice.

La modifica in chat (il testo dell'utente passato com'è al planner, come fa il logger) non tocca la riga 2, ma la riga 1 sì. Il prompt deve anche saper distinguere i due casi, quindi ho lasciato l'entrance intera in attesa. Ho scritto entrambe le righe nel ticket, che ora è `needs-info`.

Restano aperte, e le lascio a te:
- **Il charter del planner** è incompleto: il brief ora dichiara anche lo slot di partenza o il mesociclo da modificare, e gli input hanno `starting` e `changing`. Nessuna riga si è spostata, ma il testo del charter non lo dice e il charter lo modifichi solo tu.
- **La chiusura del ticket**: `/code-review` va lanciato da te, la ROADMAP non l'ho segnata e il ticket non l'ho cancellato, perché il ticket non è chiuso. Senza git non ho potuto fare nemmeno il commit, anche se mi hai indicato `674648c`.