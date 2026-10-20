---

## Ticket proposto: `docs/work/09-the-report-in-the-chat/issues/06-the-contract-the-document-is-emitted-under.md`

**Titolo**: *The contract the document is emitted under, not the reading* — `ready-for-agent`.

Ho messo nel ticket le tre correzioni che si possono fare senza toccare nessuna linea del charter, nell'ordine in cui vanno fatte, e il passaggio a pagamento in mezzo:

1. **Il prompt dice di `assumed` quello che dice il charter.** `coach/logger.py:127` vieta `assumed`, e sei righe sotto (`:133`) lo ammette dove il piano tace — che è anche quello che rifiuta il validator e quello su cui è scritto il set (48 `assumed` nei documenti attesi). Il prompt è più severo del codice che descrive.
2. **L'uguaglianza del documento si misura sul documento che scrive il motore**, i blocchi di `to_performed`, non sulla forma emessa confrontata campo per campo e blocco per posizione. Cosa lasciare fuori perché ci pensi l'aderenza è una decisione che il charter lascia al modello: uno scorer che fa pagare una delle due emissioni legali e non la sua gemella se l'è presa. È il rescoring che porta i 50 run validi da 7 a 30.
3. **Il vocabolario delle esclusioni arriva nel contesto, letto dai dati** (`movement_pattern` e i joint dal catalogo), risolto dal chiamante come già risolve quale workout è aperto. Il menu l'ha già chiuso `classify`; è la prima volta che il contesto lo dice. I sei tool restano sei.

Poi un solo passaggio a pagamento, con il numero e il drop per riga da scrivere in 05 — budget da concordare prima della prima chiamata. Come quinto punto, **solo se il drop lo dice**, i valori del blocco diventano opzionali (la regola di `load_kg` estesa a `rounds`, `rest`, `amount`), così un numero che l'utente non ha dato non va più copiato dalla prescrizione.

### Quello che il ticket non fa — serve la tua decisione

**«A refusal ends the run»** è nel charter sotto *Constrained*: il documento viene registrato come rifiutato e il modello non ha un secondo tentativo. Il planner fa l'opposto (`FEEDBACK`, `ATTEMPTS = 3`), e l'asimmetria è reale: i rifiuti di questo passaggio sono errori di documento che il validator nomina in una frase, cioè esattamente ciò da cui il planner si ripara.

Spostare quella linea comprerebbe i run falliti su una provenance o una forma che il modello avrebbe potuto correggere. Cambierebbe però cosa significa una riga tenuta (*tenuta entro tre tentativi*) e costerebbe una chiamata al modello per riparazione. Il charter lo cambi solo tu: non l'ho modificato e non ho messo la riparazione nel ticket.

Ho anche cambiato la riga `Blocked by:` di 05, che diceva «nothing now»: ora punta a 06, perché il 100% che chiede non è raggiungibile prima.