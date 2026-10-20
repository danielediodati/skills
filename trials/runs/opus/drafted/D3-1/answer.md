Non ho cambiato niente. Per rispettare la tua richiesta bisogna spostare una linea di un charter, e quella decisione spetta a te.

## Dove si blocca «oggi faccio il core ma niente gambe»

Nella fixture la rotazione è: 1 = gambe + core, 2 = petto/spalle/braccia, 3 = schiena/braccia. Nessun allenamento del ciclo è solo core, e ogni strada è chiusa dal codice:

| Strada | Cosa la blocca |
|---|---|
| L'entrance passa i gruppi «core» | `adaptation_requested` rifiuta `asked.groups`: *«name it by its number in the cycle»* (`src/trainer/plan.py:507`). |
| Sceglie il workout 1 (gambe + core) | Il validator pretende un esercizio per ogni gruppo (`every_group_trained`, `plan.py:995`), quindi le gambe entrano per forza. |
| Sceglie il 2 o il 3 | L'insieme degli esercizi ammessi è limitato ai gruppi di quell'allenamento, quindi il core non entra. |
| Il planner legge «solo core» da `said` | Il charter del planner tiene i gruppi in mano al codice: vengono dall'allenamento del ciclo e il validator li controlla. |

Il problema non sta nelle regole aggiunte una alla volta. Il modello di partenza è «un adattamento parte da uno degli allenamenti del ciclo» (ADR-0008, punto 6, e la spec della sessione 14). Finché resta così, ogni frase che non corrisponde a un allenamento del ciclo finisce in un vicolo cieco, e un'altra regola sposta solo il vicolo.

## Le due linee possibili

**A — consiglio questa. I gruppi di questo allenamento li dici tu.** `adapt_this_workout` riceve un campo `groups`, letto dalle tue parole come già succede per `minutes` ed `equipment`. Il codice continua a controllarli: insieme ammesso e almeno un esercizio per gruppo, ma sui gruppi che hai chiesto tu e non su quelli dell'allenamento del ciclo.
- Cosa ottieni: «core ma niente gambe», «solo braccia oggi», «gambe e spalle» diventano tutte richieste valide, e la legalità resta controllata al 100% dal codice.
- Cosa si sposta:
  - charter dell'entrance: un campo in più, e l'entrance decide i gruppi di questo allenamento, oggi decisi dal codice tramite l'allenamento del ciclo;
  - ADR-0008, punto 6: l'adattamento non parte più per forza da un allenamento del ciclo;
  - la riga sulla spec della sessione 14.
- Si toglie una regola (il rifiuto di `asked.groups`) e non se ne aggiunge nessuna.

**B — i gruppi li decide il planner leggendo `said`.** Negli adattamenti il codice smette di controllare i gruppi.
- Cosa ottieni: il massimo di libertà.
- Cosa si sposta: il vincolo sui gruppi del charter del planner. Quel controllo era stato spostato nel validator proprio perché Haiku lo sbagliava (ADR-0011), quindi questa strada riapre un errore già misurato.

## Cosa serve da te

1. A, B, o un'altra strada.
2. Se scegli A, l'ok a modificare il charter dell'entrance e l'ADR-0008. Il charter lo cambi tu, oppure mi dai esplicitamente il permesso di farlo.

Dopo la tua scelta lo costruisco e lo verifico con test locali, senza spendere crediti. Una passata `--suite adapt` a pagamento la proporrò a parte, con la stima del costo.

Un comando shell per leggere i log `out*.log` è stato bloccato dai permessi. L'unico che ho aperto a mano, `out5.log`, era vuoto. La diagnosi viene dal codice, dai charter e dal ticket 04.