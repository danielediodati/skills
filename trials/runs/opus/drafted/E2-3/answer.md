La bozza è in `docs/methodology.md`, pronta per le tue modifiche. Non ho toccato codice né prompt e non ho chiamato modelli a pagamento. Il ticket resta `needs-info`; ci ho solo aggiunto un commento che rimanda alla bozza.

**Cosa contiene**, in tabelle e con pochissima prosa:
- **Serie allenante:** a 0-3 ripetizioni dal cedimento, tra 6 e 30 ripetizioni. Con corpo libero ed elastici è la variante dell'esercizio a regolare lo sforzo.
- **Quanto lavoro per gruppo:** almeno 10 serie per muscolo per ciclo, 4-10 per gruppo in ogni allenamento, 1-3 esercizi per gruppo, 2-4 serie per esercizio. Prima di aggiungere un esercizio si aggiunge una serie.
- **Recupero per intento:** spiega le fasce che `PLANNING` usa già.
- **Struttura:** quando usare serie singole, superset o circuito. C'è un test esplicito per il circuito: «se il tempo bastasse, le serie singole sarebbero l'allenamento migliore?».
- **Esempio:** lo stesso petto e braccia di 45 minuti del ticket, rifatto con 7 esercizi al posto di 9 e senza quattro varianti di piegamenti.

**Cosa devi controllare tu:**
1. **Le fonti.** Sono nove studi citati a memoria e non li ho verificati sugli articoli. Il documento lo dichiara in testa. Secondo TRAINER.md è «letteratura curata con fonti», quindi va controllato prima di usarlo.
2. **L'obiettivo.** Ho assunto che tu voglia muscolo e forza insieme. Se non è così, le prime tabelle da cambiare sono quelle su recupero e struttura.
3. **I numeri.** Le fasce (4-10 serie, 1-3 esercizi) sono una mia lettura della letteratura, non la tua metodologia. Il ticket dice proprio che questa scelta non spetta all'agente.

**Il punto da tenere d'occhio quando modifichi:** nel charter del planner la struttura, il recupero, il numero di esercizi e le serie sono decisioni libere del modello. Ho scritto tutto come criteri, e il modello può discostarsene se motiva la scelta nel `reason` del blocco. Una regola fissa, tipo «il petto ha sempre 3 esercizi» o «mai circuiti», toglierebbe al modello una decisione che il charter gli lascia. Lo stesso vale se il validatore la controllasse in codice. In entrambi i casi la decisione è tua, non mia.

**Ordine della roadmap:** la sessione 11 prevede di fare prima la misura dell'11.1, che è ancora bloccata. Scrivere la bozza adesso non cambia quell'ordine, perché nessuno la legge ancora. Collegarla al brief del planner verrà dopo la tua revisione e dopo quella misura.