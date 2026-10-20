# Ticket 15c.1: costruito in parte, poi mi sono fermato su una linea del charter

Il ticket resta aperto. Le righe *«ok»* e *«no»* della tabella chiedono di spostare una linea del charter dell'entrance, e quella decisione spetta a te.

## La linea

`evals/entrance/charter.md`, sezione **Constrained**: *«The handoff set is closed (`HANDOFFS`, seven tools)»*. Perché *«ok»* accetti e *«no»* rifiuti passando da `Negotiation.answer`, il modello deve poterlo segnalare. Servono quindi due handoff nuovi, per esempio `accept_plan` e `turn_down_plan`, senza argomenti: il codice passerebbe il testo dell'utente parola per parola, come fa già `log_workout`. Così i tool diventerebbero nove, e decidere se un messaggio scritto risponde al piano diventerebbe una nuova voce in **Free**.

- **Cosa compra:** le righe 1 e 2 della tabella e le relative righe del set di eval.
- **Cosa serve da te:** modificare il charter oppure dirmi un'altra strada. Io non l'ho toccato.

## Cosa è stato costruito

- **Nuova fine `set aside`.** Ho scelto una fine nuova e non `stopped`, perché `stopped` indica un piano fermato prima di essere offerto. L'ho scritta in CONTEXT.md (Ending) e in un emendamento all'ADR-0007.
- **Nuova richiesta sopra una proposta aperta** (*«senza panca»*, *«ho 20 minuti»*): la proposta aperta finisce `set aside` e il nuovo run la segue nella stessa negoziazione.
- **Report del giorno che un'adattazione adatta:** l'adattazione finisce `set aside`. Un tap dopo non scrive niente e la chat dice che il piano è superato. Prima il tap sollevava un errore e la chat rispondeva con il messaggio fisso `FAILED`.
- **L'entrance vede la proposta aperta.** È un'aggiunta al prompt sul modello di `MID_PLAN`, che oggi copre solo le righe 3, 4 e 5.
- **Bottoni:** restano *Va bene* e *Non mi va*; *Solo 30 minuti* è tolto, insieme al `minutes` del rifiuto nel planner, rimasto senza chiamanti.
- **Il `cut` aveva un'altra causa.** `trainer runs` leggeva come `cut` ogni piano in attesa: prendeva come run vivo il thread dell'entrance, che dopo aver passato la richiesta al planner non ha né fine né domanda pendente. L'ho corretto in `runs.live`.

## Criteri di accettazione

| Criterio | Stato |
|---|---|
| Ogni riga su modelli scriptati | righe 3 e 4 coperte da test, con i record nell'archivio; riga 5 coperta solo per un report non legato al piano; righe 1 e 2 non fatte |
| Report → adattazione chiusa, tap dopo senza effetto | ✅ test `test_reporting_the_day_an_open_adaptation_adapts_ends_it` |
| Nessun `cut` dopo una nuova richiesta | ✅ test sull'archivio letto come `trainer runs` |
| Righe in `eval-set.toml` + passaggio a pagamento | non fatto: dipende dalla decisione sul charter. Prima di qualsiasi chiamata a pagamento ti propongo un budget unico per il ticket, con una stima |

## Dove siamo

- **Test:** 1915 passati, 3 falliti. Erano 3 falliti anche prima delle mie modifiche (1906 passati). Sono i tre test sulla conferma dell'esclusione in `test_bot.py`: usano una data di re-test fissa, `2026-10-15`, che oggi è già passata. Non c'entrano con questo ticket e non li ho toccati; si sistemano ricavando la data da oggi, se vuoi lo faccio.
- **mypy:** pulito.
- **Chiusura:** la directory non è un repository git, quindi niente commit né hash. Non ho fatto nemmeno `/code-review` né gli altri passi di chiusura, perché il ticket non è chiudibile.

Per il permesso negato sono stati bloccati due comandi: un `sed -i` sui test e una pipe con `grep`. Ho fatto le stesse cose con gli strumenti di modifica, quindi non manca niente.