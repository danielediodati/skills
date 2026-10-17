Ho scritto il ticket. Nessun comando eseguito contro un provider: la proposta sta tutta su quello che la pass ha già detto e su quello che il codice mostra.

---

# 📋 Ticket 9.6 — proposto
### `docs/work/09-the-report-in-the-chat/issues/06-the-contract-the-logger-emits-against.md`

**La tesi**: 24 su 90 non è un problema di lettura. Il rescore (7 → 30 sui 50 run determinati) dice che il modello legge il report; perde sulla forma in cui deve scriverlo.

## Le tre contraddizioni, verificate nel codice

| | dove |
|---|---|
| La forma esige ogni valore nel blocco, il prompt vieta `assumed` | `tools.strict_schema` (`required` su tutto) contro `logger.LOGGING` righe 127-132 — e U2/U16 del set si aspettano esattamente `assumed` sul valore prescritto |
| Un rifiuto chiude il run | `logger.validate` va a `END` con `REFUSED`; `planner.validate` rimanda le violazioni al modello con `ATTEMPTS = 3` |
| Il vocabolario delle esclusioni non c'è | nel contesto solo i due esempi del prompt; `logger.KEEPS` non porta né `movement_pattern` né `loaded_joints`, quindi nemmeno un risultato di tool lo mostra. U16 pretende `lumbar spine`, valore del catalogo |

La regola che il prompt deve dire è quella che `log.validate` **già** applica: `_nothing_assumed_the_prescription_does_not_say` rifiuta solo la *contraddizione*, non il silenzio. Quindi è il prompt che si allinea al validator, non una licenza nuova. U1 non si muove: niente è deviato, `blocks` resta vuoto.

## Due decisioni che ho preso per iscritto nel ticket

- **Il punteggio non cambia.** Il rescore resta una *nota* accanto al numero (dove `_notes` tiene i fatti che non sono failure), perché la nota U1 del set chiama «la risposta sbagliata più comune» proprio il documento che ricopia la prescrizione, e il 05 tiene gli invarianti alle righe del set.
- **La barra non è di questo ticket.** 30 su 50 è il 60% con il contratto già scontato: quello che resta è un fatto su `gpt-oss:20b`, e la scelta del provider (`qwen3.5:9b`, `LLM_BACKEND=groq`) è del 05, sulla pass «su entrambi».

Ho anche messo `Blocked by: 06` sul 05, che prima diceva «nothing now».

## Una cosa che decidi tu

La regola di slicing dà **cinque issue per sessione** e la 9 ne ha già cinque numerate (la 04 ritirata). Questo è il sesto file. Le alternative erano infilare il lavoro dentro il 05 — ma sono prompt, schema di emit, un ciclo nel grafo, stato e record: è un ticket, non una riga di prompt — o aprire una sessione per un ticket solo, che rompe la regola del demo. **Consiglio di accettare la sesta riga nella 9**; la metto in ROADMAP.md alla chiusura, non adesso.

Una nota: un comando che usava `xargs` per elencare le dimensioni dei file è stato bloccato dai permessi; ho ottenuto la stessa cosa con gli strumenti di ricerca, non ha cambiato nulla.