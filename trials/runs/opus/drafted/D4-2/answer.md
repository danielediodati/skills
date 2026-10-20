# Ticket 15c.1: fatto in parte, fermo su una linea del charter

Il ticket non è chiuso. Ho fatto tutto quello che non sposta linee del charter. Le righe 1–2 (*«ok»* accetta, *«no»* rifiuta) richiedono una tua decisione.

## Cosa serve decidere

`evals/entrance/charter.md` tiene come **vincolata** la superficie chiusa delle *sette* handoff. Tra le scelte **libere** del modello non c'è accettare o rifiutare un piano. Oggi un piano lo accetta solo un tap che porta l'id della proposta. Far leggere *«ok»* all'entrance vuol dire dare al modello quella decisione, che scrive un allenamento o tiene un mesociclo. Quindi la linea si sposta.

- **Cosa compra:** si risponde a un piano scrivendo, che è proprio la cosa che ti mancava sul demo.
- **Come la farei, se la sposti tu:** due handoff (`accept_proposal`, `turn_down_proposal` con `said`), offerte solo mentre c'è una proposta aperta. Passano dallo stesso `Negotiation.answer` del tap, con l'id letto dal codice e mai dal modello. Il charter va aggiornato da te: le due handoff tra le scelte libere, l'id e il passaggio da `answer` tra i vincoli.

## Cosa è stato costruito

- **Una proposta chiusa senza risposta ora ha un finale.** Prende `stopped`, un finale che esiste già: niente finale nuovo, perché in tutti e due i casi la run è stata superata prima della risposta. Ho aggiornato CONTEXT.md (Ending) e ADR-0007 punto 7.
- **Una nuova richiesta sopra una proposta aperta resta nella stessa negoziazione** e segue la run chiusa. Nessuna run in archivio risulta più `cut`.
- **Riportare l'allenamento che un adattamento adatta chiude l'adattamento.** Un tap dopo non cambia niente e la chat dice perché (con la situazione `SUPERSEDED`). Il controllo vale anche se il report arriva da `trainer log`.
- ***Solo 30 minuti* è sparito:** ora ci sono due bottoni per allenamento e mesociclo. Ho aggiornato README e TRAINER.md.

## Verifiche

- **Test:** 1913 passati, mypy pulito. Ci sono 6 test nuovi, a livello di negoziazione e di bot, per le righe 3 e 4 e per il tap a vuoto. Ne ho tolti 2 che riguardavano il bottone dei 30 minuti.
- **Criteri di accettazione:**
  - Il 2 è verificato.
  - Il 3 è verificato per i casi coperti dai test.
  - L'1 è verificato solo per le righe 3–5.
  - Il 4 (eval a pagamento) non è partito: prima dobbiamo concordare un budget, e le righe da aggiungere al set dipendono dalla tua decisione.

## Cosa si è rotto rispetto a prima

- **Bottoni *Solo 30 minuti* già in chat:** quelli inviati da `1.0.0rc1` ora vengono ignorati senza nessuna risposta, perché l'azione `30` non è più riconosciuta.

## Cosa manca

- **Niente commit:** la cartella non è un repository git, quindi niente hash.
- **`/code-review` non l'ho potuto lanciare.**
- **Ticket aggiornato:** l'ho lasciato con `Status: needs-info`, una sezione su cosa è fatto e cosa aspetta te.
- **Comandi negati:** alcuni comandi shell composti sono stati bloccati, senza conseguenze sul lavoro.

C'era una sorpresa nei test di partenza: 3 test del bot sulle esclusioni fallivano già prima del ticket. `proposing` usava una `retest_date` fissa al 15/10, ormai passata. Ora la data è relativa a oggi.