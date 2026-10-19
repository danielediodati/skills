Ticket scritto: `docs/work/09-the-report-in-the-chat/issues/06-the-contract-the-log-pass-failed-on.md`.

**Cosa propone di costruire** (le tre cose che la pass ha trovato e che si possono fare senza toccare il charter):

1. **Un valore che nessuno ha dato si lascia fuori.** `amount`/`rounds`/`rest` e le loro provenance diventano nullable a coppie — la regola che `load_kg` ha già — e `to_performed` riempie il null dal blocco prescritto che `_paired` ha agganciato, marcandolo `assumed`. È ciò che il charter dice già che faccia il codice: oggi la forma lo rende impossibile, e il modello deve copiare dalla prescrizione e etichettare.
2. **Il vocabolario delle esclusioni letto dai dati** (`movement_pattern`, `loaded_joints`) e messo nel prompt, letto all'apertura della run e non al build. Il modello continua a decidere se proporre e cosa nominare; la granularità resta di `classify`.
3. **Punteggio sul documento che scriverebbe il motore**: `_difference` confronta i due lati risolti da `to_performed`, come già fa il controllo sul volume. Le righe del set non cambiano. Siccome sul documento risolto «prescrizione ribadita» e «documento vuoto» diventano la stessa cosa, la regola del set *only the deviations are written* diventa un fallimento a sé (un blocco che non rivendica nulla di proprio), così U1 resta coperta.

**Due linee che non ho spostato**, e che restano decisione tua — sono nel ticket sotto *What is not built*:

- **Il rifiuto chiude la run** (charter, *Constrained*: *the planner replans; this does not*). Un campo sbagliato costa l'intera riga, allenamento letto bene compreso. Rimandare il rifiuto al modello comprerebbe quelle righe; il punto 2 toglie la causa più frequente del rifiuto, che è la parte costruibile senza toccarla.
- **`assumed` non è mai del modello** (charter, *Constrained*). Dove un blocco non si appaia a nulla di prescritto — una sostituzione, U6 — nessuno può riempire il valore: il codice non ha una controparte da cui leggerlo. Il set si aspetta `rest: 150, "assumed"`, e il docstring di `log._nothing_assumed_the_prescription_does_not_say` lo chiama l'etichetta onesta proprio in quel caso. Set, ragionamento del validator e charter non concordano su quella cella: **U6 non è tenibile da nessun agente** finché non decidi tu. Permettere `assumed` *solo* dove la prescrizione tace la comprerebbe.

**Due cose che non ho fatto e che servono se accetti il ticket**: una voce 9.6 in ROADMAP.md (senza, il passo 6 della chiusura non ha dove scrivere l'hash) e la riga `Blocked by: 06` su 05, che oggi dice «nothing now». Dimmi se le aggiungo.