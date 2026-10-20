---

# ⚠️ Ticket 10.3: costruito, non chiuso
### Una richiesta per oggi adatta l'allenamento del giorno; una richiesta per il futuro riscrive il mesociclo senza azzerare i cicli
`nessun commit` · 1554 test · mypy pulito · niente rotto

---

**Perché non è chiuso.** I primi tre criteri dipendono da come il modello legge le frasi, e da questa sessione non ho potuto raggiungere un modello vero: l'accesso alla rete e all'ambiente è stato negato. In più la cartella non è un repository git (il `674648c` della richiesta non esiste qui). Quindi mancano il commit, l'hash in ROADMAP e la cancellazione del ticket. Non ho cancellato il ticket: senza commit il ragionamento andrebbe perso, e l'ho scritto nei suoi *Comments*.

## Cosa è stato costruito
L'entrance ha due nuovi handoff, `adapt_today` e `change_mesocycle`. Il prompt le dice di chiedere *«solo oggi o d'ora in poi?»* quando non riesce a capirlo. Un adattamento parte dallo slot di oggi del mesociclo; quando viene accettato diventa il serving di quello slot, sostituisce un serving non ancora eseguito e lascia il mesociclo com'era. Una modifica sostituisce il mesociclo attivo e conserva il conteggio dei cicli. Il validatore rifiuta una modifica identica all'originale o con un numero di cicli inferiore a quello in corso.

## Cosa puoi lanciare
```
$ uv run trainer plan --change "basta affondi" --workout 2
Error: --change plans every slot of the split, so it names none: drop --workout and --group
```
- `trainer plan --time 30` (oppure `--equipment`, `--exclude`, `--avoid`) adatta l'allenamento di oggi se c'è un mesociclo in corso. Se non c'è, pianifica un allenamento da zero come prima.
- `trainer plan --change "no more lunges" --exclude lunge` riscrive il mesociclo. Con `--exclude` il validatore garantisce che gli affondi non tornino.

Non ho potuto lanciare questi due comandi su dati veri: avrei dovuto aprire la tua home reale `~/.reps`, e non ho potuto crearne una di prova. Li ho verificati solo nei test, con modelli scriptati.

## Cosa si è rotto rispetto a prima
Nulla di mio. Tre test del bot erano già rossi prima di toccare il codice: usavano una data di retest fissa (`2026-10-15`) che l'orologio ha superato. Li ho corretti.

## Dove siamo
- **Test e tipi:** 1554 test verdi, mypy pulito.
- **Criteri:** spuntato solo il quarto. Per i primi tre la catena funziona con un modello scriptato, ma la lettura del modello vero non è verificata.
- **`/code-review`:** non posso lanciarlo da qui. L'ho sostituito con una revisione mia: un problema corretto con un test, uno lasciato com'è per scritto.
- **Per chiudere servono:** un giro reale con *«solo 30 minuti oggi»*, *«basta affondi»* e una frase ambigua, poi il commit `Close ticket 10.3`, l'hash in ROADMAP e la cancellazione del ticket.
- **Sbloccato:** il ticket 05, a cui ho aggiunto un vincolo (sotto).

Una cosa da sapere: gli handoff restano senza argomenti, come vogliono ADR-0006 e il suo test. Al planner arrivano le ultime tre frasi dell'utente così come le ha scritte. Quindi in chat un *«solo 30 minuti»* scritto a parole viene rispettato dal modello ma non controllato dal validatore. Il bottone *Solo 30 minuti* e `--time 30` invece vengono controllati. Ho scritto questo vincolo nel ticket 05, perché va misurato lì.