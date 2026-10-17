Ho scritto la proposta come ticket 06 della sessione 9: `docs/work/09-the-report-in-the-chat/issues/06-the-contract-the-document-arrives-under.md`, e ho messo 05 `Blocked by: 06` — altrimenti un agente lo prende e rimisura il contratto invece del modello.

**Le quattro cose, nell'ordine in cui pesano**

| # | difetto | dove | costo |
|---|---|---|---|
| 1 | lo scorer penalizza una forma che scrive la stessa riga | `log_evaluation._difference` | 23 run su 50 |
| 2 | il prompt vieta `assumed`, la forma lo impone e il set lo aspetta | `logger.LOGGING` | ogni blocco con un valore non detto |
| 3 | un rifiuto chiude la run, quello del planner torna al modello | `logger.build.validate` | la run, contata come *not run* |
| 4 | il vocabolario delle esclusioni non è in nessun contesto | `logger.brief` | U13-U16 |

Il punto che tiene insieme 1 e 2: `tools.strict_schema` rende obbligatoria ogni proprietà, e `PerformedBlock` chiede comunque `rounds`/`rest` con le loro provenance. **Un blocco si può omettere intero, un valore dentro un blocco no** — quindi *"solo 2 serie di militari"* deve portare il riposo che nessuno ha detto, e `assumed` sul valore prescritto è l'unica etichetta vera (CONTEXT.md § Provenance; `log.py` rifiuta solo l'`assumed` che la prescrizione *contraddice*). Il prompt dice il contrario in due righe e poi se lo rimangia due righe dopo.

**Due decisioni che puoi ribaltare, perché cambiano cosa misura la suite**

- **Punteggio sul documento che l'engine scriverebbe** (`to_performed` su entrambi i lati, blocchi confrontati senza ordine quando c'è una prescrizione dietro). È quasi tutto il 7→30. Il prezzo: un documento che ricopia tutta la prescrizione ora tiene. Lo faccio pagare in `_notes`, non nel punteggio — *N run su M hanno ricopiato la prescrizione; non scored, e nemmeno gratis*. È lo stesso argomento che `_filled` fa già nella metà delle domande, quindi metà suite legge così da quando è nata. Richiede però di correggere `docs/logging/eval-set.md` § How to read a row: nessuna riga cambia, cambia cosa è *scored*.
- **Vocabolario nel brief, non in `logger.KEEPS`**: i 12 pattern e i 7 joint letti dal catalogo (`catalog.values`, `catalog.joint_values`), una volta per run. Aggiungere `movement_pattern`/`loaded_joints` a ogni esercizio letto è contesto pagato a ogni turno senza una riga che fallisce dietro. Se dopo il passaggio U13-U16 ancora mancano, quello è il prossimo posto dove guardare.

La barra resta 100%: tre dei quattro interventi rendono misurabile un agente corretto, il quarto gli dice una cosa vera che non sapeva. Quanto tiene dopo è il numero di 05.

Verifica senza provider: i 90 record della passata fallita contengono il documento emesso (`record.of` → `performed`) e le domande, quindi il riscoring si fa offline e il 7→30 è riproducibile. Al provider il ticket paga due righe sole, `--only U13 --only U2`.