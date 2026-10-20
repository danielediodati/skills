---

## Ticket proposto — `docs/work/09-the-report-in-the-chat/issues/06-the-contract-the-logger-emits-against.md`

**Status**: `ready-for-agent` · **blocca 05** (che diventa `Blocked by: 06`) · riga aggiunta in ROADMAP come item 6, *prima* del 5.

### Perché un ticket separato e non dentro il 05
Il 05 è *la misura*. Le quattro cose che hanno fatto 24/90 sono codice, schema e prompt: se stanno nel 05, è la misura che salta quando finisce il contesto. Così il 06 chiude su test offline e il 05 resta la riga che scrive il numero.

### Le quattro cose, come le ho verificate nel codice
| # | dove | cosa |
|---|---|---|
| 1 | `tools.strict_schema` + `logger.LOGGING` | lo schema rende obbligatori `rounds`, `rest`, `amount` e i loro `_source`: un numero mai detto va copiato dalla prescrizione ed etichettato. Il brief dice *"Never `assumed`"* nove righe prima di dire *"A number marked `assumed` has to be the prescribed one"*. Il set si aspetta `assumed`, `log.validate` lo accetta |
| 2 | `logger.after_validate` | rifiuto → `END`. Il planner ha `FEEDBACK` + `ATTEMPTS` e torna al modello. Nella suite un rifiuto perde la riga due volte (`VALIDATOR` e `DOCUMENT`) |
| 3 | `logger.KEEPS`, `search_exercises` | `ProposedExclusion.value` deve essere un `movement_pattern` o un `loaded_joints` carattere per carattere, e nessuno dei sei tool lo porta in contesto. Sei righe dipendono da quella stringa |
| 4 | `log_evaluation._difference` | confronta il documento *emesso*, partendo da `len(blocks)`. `_produced` già costa quello risolto — `DOCUMENT` rosso con `VOLUME` verde è la firma del problema |

### Due dettagli che altrimenti il rescore non si riproduce
- **I blocchi risolti si confrontano per esercizio, non per posizione**: `to_performed` mette prima i blocchi nominati nel report, quindi l'ordine è un fatto sulla frase. Eccezione U8 (`workout_id: null`), dove l'ordine è l'unica cosa che dice *"poi"*.
- **Le trenta righe non si toccano**: cambia solo dove si misura, e con esso `eval-set.md`, il docstring di `log_evaluation.py` e l'help di `trainer eval`.

### Cosa il ticket si rifiuta di fare
Non rende nullabili `rounds`/`rest` in `log.py` (renderebbe vera la regola *un valore che nessuno ha dato si omette*, ma riscrive ogni documento atteso di un set scritto in cieco: è un ADR, non questo ticket). E non promette una percentuale: la chiusura chiede quattro righe su Groq come sanity check, il numero vero è il 05.

Due note che potresti voler ribaltare: è un **sesto** item in una sessione che la slicing rule tiene a cinque (il 4 è ritirato, quindi cinque vivi), e la metà *must-ask* resta sporca finché non cade il punto 1 — un `reported` forzato su un numero prescritto è una *false confidence* che `_filled` conta doppia.