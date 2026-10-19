Ticket proposto, non implementato: `docs/work/09-the-report-in-the-chat/issues/06-the-logger-is-told-to-break-its-own-contract.md` (Status: `needs-triage`).

## Cosa dice

**Le due cose costruibili subito**, senza toccare niente di riservato dal charter:

1. **Il prompt contraddice schema, validatore e set.** `coach/logger.py:126` vieta `assumed`, `:135` lo richiede al valore prescritto, `:130` dice di «lasciare fuori» un valore che lo schema strict rende obbligatorio (`tools.strict_schema`, `tools.py:587`). Il set si aspetta `assumed` in nove righe su diciotto. Un modello che crede al prompt può solo scrivere `reported` — cioè far dire all'utente una cosa che non ha detto — o non scrivere il blocco. È anche la spiegazione più probabile della perdita nella metà must-ask: senza «lasciare fuori» dentro un blocco, chiedere è l'unica strada onesta, e il prompt ne indica una terza che non esiste.
2. **Il vocabolario delle esclusioni non è nel contesto.** `brief` porta data e workout aperto, `KEEPS` taglia via `movement_pattern` e `loaded_joints`, il prompt dà due esempi. U13-U16 vogliono `shoulder`, `vertical push`, `knee`, `lumbar spine` carattere per carattere. Si legge dal catalogo, con un solo reader condiviso con `classify`, mai una lista in Python.

**Le tre decisioni che ho lasciato a te**, con la riga nominata invece di spostata:

| decisione | riga | cosa comprerebbe |
|---|---|---|
| turno di riparazione dopo un rifiuto | charter § Constrained, *no repair turn* | le 4 run che non hanno prodotto nulla da valutare, e un tentativo invece di un `VALIDATOR` in più; costa una emit call per run rifiutata |
| forma emessa che non obbliga ogni valore | stessa riga, *every property required* | il documento potrebbe dire *questo l'utente non l'ha detto* per omissione, ed è la forma che servirebbe a U7 |
| cosa misura la suite | `docs/logging/eval-set.md` | è il 7 → 30: ma è lo standard scritto in cieco, e cambiarlo dopo la prima passata misura l'autore |

**La mia raccomandazione**: non toccare lo scorer in questo ticket. Sistema il prompt, rilancia (locale, gratis, ore di orologio), e decidi con il secondo numero in mano — se il modello emette la forma per sola deviazione che il set si aspetta, l'uguaglianza regge e non si sposta niente.

Due note: il ticket è un sesto in una sessione che ne ammette cinque — l'alternativa è portarlo come seconda metà di 05 e chiudere entrambi sulla riga di roadmap di 05, ed è una tua decisione. E 05 non può chiudersi prima di questo.