Non ho modificato niente: l'unica soluzione sposta una linea dei charter, e quella decisione spetta a te.

**Perché è un vicolo cieco.** Lo split della fixture è `[legs, core]`, `[chest, shoulders, arms]`, `[back, arms]`. Oggi tocca allo slot 1. Per «oggi faccio il core ma niente gambe» il codice offre tre strade, e tutte e tre falliscono:

| strada | perché fallisce |
|---|---|
| tenere lo slot 1 | il validator rifiuta un piano che non allena le gambe (`every_group_trained`) |
| `workout=2` o `3` | in quegli slot non c'è il core, e il set ammissibile filtrato sui gruppi non contiene nemmeno un esercizio per il core |
| `leave_out` | accetta solo id di esercizi: non può togliere un gruppo intero |

`adaptation_requested` rifiuta anche i `groups` in modo esplicito (`plan.py:507`). Qualunque regola in più aggiungerebbe solo un altro caso speciale dentro questo stesso perimetro. Il problema è il perimetro: oggi in un adattamento i gruppi li decide sempre lo slot, mai l'utente.

**La linea da spostare.** I gruppi di questo allenamento devono venire dalle parole dell'utente. Oggi non è possibile per quattro motivi:
- ADR-0008 item 6 e la spec 14 dicono che un adattamento parte *da uno dei workout del mesociclo*;
- il charter dell'entrance elenca come liberi solo cinque argomenti di `adapt_this_workout` (`minutes`, `equipment`, `leave_out`, `ask_for`, `workout`);
- il charter del planner prende i gruppi da quello che dice una porta e, se nessuno li nomina, dalla rotazione. Su questo punto la modifica non lo contraddice;
- `adaptation_requested` scarta i `groups` se l'entrance prova a passarli.

**Cosa propongo.** Aggiungere un argomento `groups` ad `adapt_this_workout`: tutti i gruppi di questo allenamento, letti da quello che ha detto l'utente, come già succede con `equipment`.
- La richiesta la costruisce sempre il codice (`plan.requested` accetta già `Asked.groups`, come fa il terminale).
- Il validator resta com'è: allena ogni gruppo nominato e sceglie solo nel set ammissibile di quei gruppi.
- La volontà dell'utente decide che cosa si allena oggi. Il codice controlla soltanto che il piano lo rispetti.
- Si semplifica anche la riga del calcio: «niente gambe» diventa `groups` senza legs, e l'entrance non deve più indovinare il numero dello slot.

Sconsiglio l'alternativa di far scegliere i gruppi al planner leggendo `said`. Il validator controllerebbe il piano contro una richiesta scritta dal modello stesso, e questo sposta la linea «la richiesta la costruisce il codice, mai il modello».

**Cosa devi decidere tu:**
1. Approvi `groups` come argomento libero di `adapt_this_workout`? Se sì, il charter dell'entrance e ADR-0008 item 6 vanno aggiornati, e il charter lo modifichi tu.
2. Un allenamento adattato in questo modo conta come lo slot dovuto, quindi la rotazione va avanti di uno, oppure no?

Con il tuo sì faccio la modifica e la verifico con test locali gratuiti. La misura sull'adaptation set è a pagamento: prima ti do una stima e concordiamo il budget del ticket.