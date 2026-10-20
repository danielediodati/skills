Non ho cambiato niente: né codice, né charter. Con le regole attuali la frase non si può soddisfare, e per uscirne bisogna spostare una linea di un charter. Questa decisione spetta a te.

## Dove si blocca

Nel fixture il workout in programma è il 1, che allena `legs` e `core`. Con «oggi faccio il core ma niente gambe» succede questo:

| Cosa | Dove | Effetto |
|---|---|---|
| I gruppi li fissa il codice, presi dallo slot | planner, Constrained: «Exclusions, equipment, today's time and groups are folded into the request by code» | il prompt dice «This workout trains: legs, core … anything else is not today's workout» e subito dopo «They said: … niente gambe» |
| Ogni gruppo richiesto deve avere un esercizio primario | planner, Constrained: `untrained` | ogni piano senza gambe viene rifiutato; al terzo tentativo la run si chiude `refused` |
| L'entrance non può nominare gruppi | entrance, Constrained: «`adapt_this_workout` names no workout content, only a cycle slot number» | l'unica via d'uscita è un altro workout del ciclo, e nessuno dei tre è «solo core» |

Cambiare solo il prompt non basta: il modello seguirebbe la frase e il validatore rifiuterebbe ogni piano. Il vicolo cieco resterebbe, solo più costoso.

## Le due strade

**1. La volontà la legge il planner (te la consiglio).** In un adattamento i gruppi dello slot diventano un punto di partenza, come già succede per `allocation`. Il planner legge `said` e decide cosa allenare.
- **Linee che si spostano:** «groups folded by code» e `untrained` non valgono più per gli adattamenti. Tra le scelte libere del planner entra «quali gruppi allena un workout adattato». La legalità resta al 100%: l'enum rimane l'insieme ammissibile, con attrezzatura ed esclusioni.
- **Cosa ottieni:** qualsiasi frase su questo workout funziona («solo braccia», «un full body») senza campi nuovi e senza regole nuove. È quello che chiedi.
- **Cosa costa:** per gli adattamenti torna il rischio che ha fatto nascere `untrained`, cioè Haiku che dimentica un gruppo senza che nessuno l'abbia chiesto. Quel rischio non lo controllerebbe più il codice al 100%: lo misurerebbe l'adaptation set con una soglia.

**2. La volontà la scrive l'entrance.** `adapt_this_workout` riceve un campo `groups` e il codice lo mette al posto dei gruppi dello slot. In questo caso `untrained` continua a valere sui gruppi chiesti.
- **Linea che si sposta:** «names no workout content» nel charter dell'entrance.
- **Cosa ottieni:** i gruppi restano verificati al 100%.
- **Cosa costa:** è un'altra regola, cioè proprio quello che hai detto di smettere di fare. In più, richieste miste come «core e un po' di braccia» devono passare per una lista chiusa.

Resta aperta un'altra questione, per entrambe le strade: un giorno di solo core oggi conta come workout 1 del ciclo. Questo significa che le gambe saltano per questo ciclo.

Se mi dici quale linea spostare, e tocca a te aggiornare il charter, procedo con codice e test. Prima di qualsiasi run a pagamento concordiamo il budget.