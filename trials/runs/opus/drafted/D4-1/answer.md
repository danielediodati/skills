Il ticket 15c.1 è fatto solo in parte e resta aperto. Per la parte centrale, *«ok»* e *«no»* letti come risposta a un piano, bisogna spostare una linea del charter dell'entrance, e quella decisione spetta a te. Il resto è costruito e testato.

## La linea che va spostata

`evals/entrance/charter.md`, sezione Constrained:

> *The handoff set is closed, seven tools in `HANDOFFS` …*
> *No handoff takes an argument except `said`, on the two `CHECKED` ones.*

Oggi il modello può agire solo chiamando uno di questi sette handoff, e nessuno risponde a una proposta. Per far passare *«ok»* e *«no»* dallo stesso `Negotiation.answer` di un tap ci vuole almeno un handoff nuovo. Ci sono due modi:

| Opzione | Cosa sposta |
|---|---|
| **A** (consiglio questa): due handoff senza argomenti, `accept_proposal` e `turn_down_proposal`, offerti solo mentre una proposta è aperta | solo il conteggio "sette", che diventa nove |
| B: un solo `answer_proposal(accepted)` | il conteggio e la regola "nessun argomento" |

Con A, nel caso del *«no»* il codice passerebbe al planner il testo dell'utente così com'è come motivo del rifiuto, come già fa `log_workout`. Così il modello non deve riscrivere niente.

## Cosa ho costruito

- **Nuovo ending, `superseded`.** Lo riceve una proposta che finisce senza risposta, in due casi:
  - si apre una nuova richiesta sopra di essa (`Negotiation.open` → `end`);
  - viene registrato l'allenamento che l'adattamento adattava (`Negotiation.overtaken`, chiamato dopo il log).

  Così nessun run nell'archivio risulta più `cut`. L'ho scritto in CONTEXT.md (Ending) e in ADR-0007, al punto 7. Ho scelto un ending nuovo e non `stopped`, perché `stopped` è un piano che non è mai stato offerto.
- **Bottoni di una proposta chiusa.** Un tap non cambia niente, e la chat spiega il motivo con la Situation `SUPERSEDED`, che esisteva già.
- **Bottoni del piano.** *Solo 30 minuti* è stato tolto: ora i bottoni sono due, *Va bene* e *Non mi va*, per tutti i piani. Ho aggiornato anche la frase del README sotto "What it does".
- **Righe della tabella del ticket.** Una nuova richiesta sopra una proposta, il report dell'allenamento adattato e qualsiasi altro messaggio funzionavano già con gli handoff esistenti. Ora le prime due chiudono anche la proposta.

## Verifica

- **Test:** 1909 passano e 3 falliscono. I 3 falliti (`test_bot.py`, test sui bottoni di conferma dell'esclusione) fallivano già prima che toccassi qualcosa: la baseline era 3 falliti e 1906 passati. Non li ho indagati.
- **mypy:** pulito.
- **ruff:** non installato, quindi non l'ho eseguito.
- **Test aggiunti:**
  - 4 in `test_negotiation.py`: una nuova richiesta scrive `superseded`; un adattamento si chiude quando il suo allenamento è registrato e resta aperto finché non lo è.
  - 1 in `test_bot.py`, che copre il criterio 2 dall'inizio alla fine: report dell'allenamento → tap sul vecchio *Va bene* → la chat risponde `SUPERSEDED`, non viene scritto niente e l'archivio contiene `superseded` e nessun `cut`.
- **Test rimossi:** i 2 su *Solo 30 minuti*.

## Cosa resta prima di chiudere il ticket

1. **La tua decisione sulla linea.** Dopo, aggiungerò la riga al prompt che dice all'entrance che una proposta è aperta, il collegamento a `Negotiation.answer` e i test sui modelli scriptati per le due righe che mancano.
2. **Le righe nuove in `docs/adapting/eval-set.toml` e il passaggio a pagamento di `trainer eval --suite adapt`.** Prima concordiamo un budget per tutto il ticket, e te lo chiederò con la stima del costo.
3. **`/code-review`, commit e hash.** La cartella non è un repository git, quindi non posso fare commit né segnare il ticket come done in ROADMAP.md. Il file del ticket è ancora al suo posto.