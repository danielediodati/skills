La bozza è in `docs/methodology.md`. Il ticket 11.2 resta `needs-info` finché non la approvi.

**Cosa c'è dentro.** Ogni sezione risponde a una delle quattro domande del ticket, più l'ordine e come riempire il tempo:

| sezione | proposta |
|---|---|
| Serie allenante | 0-3 ripetizioni dal cedimento; 6-12 ripetizioni sui multiarticolari, 10-20 sull'isolamento, fino a 25-30 a corpo libero o con elastici (oltre, si passa alla variante più difficile) |
| Volume | 6-10 serie per muscolo per allenamento e almeno 10 per ciclo; 1-2 esercizi per gruppo sotto i 45 minuti; mai due varianti dello stesso esercizio |
| Recupero | le fasce di TRAINER.md con l'intento accanto; l'isolamento passa da 60 s a 60-90 s |
| Struttura | serie singole per il primo multiarticolare di ogni gruppo; superserie solo tra esercizi che non competono (per esempio agonista e antagonista); circuito solo come finisher o in un adattamento di 20 minuti o meno, mai con due esercizi sullo stesso muscolo |
| Riempire il tempo | prima si aggiungono giri ai blocchi esistenti, poi si separa una superserie, solo dopo si aggiunge un esercizio, mai una variante |

C'è anche un esempio svolto: la stessa richiesta del ticket (petto e braccia, 45 minuti, corpo libero ed elastici) costruita con queste regole. Viene 36:42 più il setup, con 9 serie per il petto e 7 a testa per bicipiti e tricipiti. L'ho calcolato con la formula di `duration.py` (3 s a ripetizione), ma il motore non l'ha mai costato. Il documento non nomina id del catalogo, solo pattern e muscoli, così il vocabolario resta quello dei dati.

**Da controllare prima di tenerla:**
- **Le fonti**: le otto citazioni sono a memoria e nessuna è verificata. Il documento lo dice.
- **I numeri sono la media della letteratura, non il tuo modo di allenarti.** È proprio la parte che TRAINER.md assegna a un umano.
- **Quattro decisioni aperte**, elencate in fondo al file:
  - i numeri del volume;
  - se vuoi i circuiti al di fuori degli adattamenti brevi;
  - cosa fare oltre le 30 ripetizioni a corpo libero, visto che il piano non ha un campo per il tempo di esecuzione;
  - come arriva al planner: dentro `PLANNING` oppure come tool.

**Cosa non ho fatto:**
- Non ho toccato il brief né il codice: quello è il lavoro vero del ticket, dopo la tua revisione.
- Non ho eseguito test.
- Non ho fatto commit: la directory non è un repository git.
- Ho aggiunto un commento al ticket che rimanda alla bozza.

**Ordine della roadmap.** La roadmap mette la misura dell'11.1 prima di questo ticket, e l'11.1 non è chiuso. Però il commento del 24/09 nell'11.3 è già un indizio forte: `gpt-oss-120b` su OpenRouter ha prodotto la stessa forma economica. Quindi la causa più probabile è il brief vuoto, non il modello locale.