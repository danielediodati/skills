La bozza è pronta in `docs/methodology.md`, da modificare come vuoi. Il ticket non è chiuso e resta `needs-info`: aspetta le tue modifiche. Non ho toccato codice, prompt o charter, e non ho speso nulla.

**Cosa c'è nella bozza**, in sette sezioni brevi:

1. **Ordine di costruzione**: prima i working set per gruppo, poi il recupero che servono, poi il minimo di esercizi che li coprono. Il tempo è una conseguenza, non l'obiettivo.
2. **Working set**: 1-3 RIR (ripetizioni lasciate in riserva prima del cedimento), 6-15 ripetizioni sui multiarticolari e 10-20 sui monoarticolari. Se un esercizio è troppo facile si passa alla variante più difficile (`regression_of` letto all'insù), non a più ripetizioni o a più esercizi.
3. **Serie ed esercizi per gruppo**, in base ai minuti del gruppo. Il primo esercizio è il multiarticolare principale. Due esercizi legati da `variant_of` contano come un esercizio solo: è la riga contro i quattro push-up.
4. **Recupero per intento**: le fasce che il prompt usa già, più superset e circuito. Il recupero non si taglia per stare nel tempo.
5. **Serie singole, superset o circuito**: quando usare l'uno o l'altro, e quando invece è solo la forma che costa meno.
6. **Piano sotto il tempo**: l'ordine in cui riempirlo, mai con un esercizio in più nel circuito. È la parte che serve al ticket 11.3.
7. **Esempio svolto**: la stessa richiesta (petto e braccia, 45 minuti, corpo libero ed elastici) con 4 esercizi e 13 working set, invece dei 9 esercizi osservati. Il motore non l'ha cronometrato.

**Da sapere prima di modificarla:**

- **Le parti segnate [?] sono mie.** Ripetizioni e RIR, le fasce di minuti per gruppo, il cedimento, i superset sullo stesso muscolo e il core sono proposte mie. Le domande sono elencate in fondo, sotto *Open for the user*.
- **Le fonti sono citate a memoria** e non le ho controllate sui paper. Vanno verificate prima di trattarle come letteratura curata, che è ciò che TRAINER.md chiede a questo documento.
- **Ogni riga è scritta come criterio per il modello, non come regola**: chi se ne discosta lo dice nel `reason` del blocco. Così la struttura resta una scelta libera del modello, come dice il charter del planner. Se vuoi che qualcosa diventi un controllo nel validatore (per esempio "mai due esercizi dello stesso muscolo in un circuito"), sposta una linea del charter e va contro ADR-0001. Si può fare, ma la decisione è tua.
- **Il catalogo con corpo libero ed elastici non ha esercizi per i bicipiti.** In quella richiesta "braccia" vuol dire solo tricipiti: l'ho scritto nell'esempio.
- **Ho aggiunto un commento al ticket 11.2** che rimanda alla bozza.

**Cosa resta da decidere:**

- **Come la bozza arriva a `PLANNING`.** La specifico dopo le tue modifiche.
- **La misura 11.1 (cioè 12.4) non è ancora stata fatta.** La roadmap la vuole prima della metodologia, per sapere se la causa è il brief o il modello. Scrivere la bozza non dipende da quella misura; collegarla al prompt sì, se vuoi rispettare quell'ordine.