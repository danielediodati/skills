Ho smesso di aggiungere regole e ne ho tolta una: in un adattamento il validatore non impone più i gruppi muscolari dello slot. L'allenamento in programma resta il punto di partenza, ma cosa si allena oggi lo decide quello che hai detto. Il cambio è verificato dai test, non ancora su un modello reale.

**Il vicolo cieco.** Lo slot 1 è gambe + core, e il validatore pretendeva un esercizio per ciascun gruppo. Per «oggi faccio il core ma niente gambe» non esisteva nessun piano legale:
- con lo slot 1 servivano per forza le gambe;
- con gli slot 2 e 3 il core non c'è;
- indicare i gruppi a mano era rifiutato.

Ogni regola aggiunta per sistemare una richiesta ne bloccava un'altra.

**Cosa ho cambiato**
- `plan.py`: in un adattamento la richiesta non porta più i gruppi dello slot né la loro divisione dei minuti. Lo slot dice solo da quale allenamento si parte e quale conta come fatto nel ciclo. Ho tolto anche il pezzo di rifiuto «dai `workout`», che senza gruppi non scattava più.
- **Cosa resta garantito al 100%:** esclusioni, attrezzatura di oggi, minuti, esercizi chiesti ed esercizi tolti. Chiedere un esercizio non lo rende ammesso se l'attrezzatura o un'esclusione lo vietano.
- Le istruzioni al planner ora dicono: «What they said comes first: it decides what this workout trains, and the workout below is only where you start».
- **Effetto collaterale voluto:** le trazioni il giorno delle gambe (riga 8 del set) ora si pianificano invece di essere rifiutate.
- La decisione è scritta in un nuovo ADR, `docs/adr/0014-in-an-adaptation-what-the-user-said-comes-first.md`, che modifica il punto 6 dell'ADR-0008. Contiene anche la regola d'ora in poi: una richiesta che fallisce si corregge nelle istruzioni al planner o nelle parole del tool, mai con una regola nuova.
- Ho aggiunto al set di adattamento la riga `core-no-legs`, che controlla che non ci siano esercizi di gambe, e ho aggiornato lo spec e il ticket 04.

**Test**
- **Suite:** 1851 passati, 3 falliti.
- **I 3 falliti** sono in `test_bot.py` (i bottoni di conferma dell'esclusione nel logger). Fallivano già prima della modifica, identici, e non toccano il planner.
- **mypy:** pulito.
- **Test riscritti:** quelli che verificavano i gruppi dello slot ora verificano il contrario. Ne ho aggiunti tre:
  - un piano con solo core sul giorno gambe passa la validazione;
  - le trazioni sul giorno gambe sono accettate;
  - un bilanciere chiesto con solo corpo libero è ancora rifiutato.
- **Non verificato:** volevo controllare che il test del core fallisse col codice vecchio, rimettendo per un attimo i gruppi. Serviva un'approvazione che in questa sessione nessuno poteva dare, quindi non l'ho visto fallire.

**Cosa non ho fatto**
- Non c'è un repository git in questa cartella, quindi non ho fatto commit.
- Non ho lanciato il set di adaptation sul modello, perché costa crediti. Ti propongo due opzioni, con stime basate sul secondo passaggio del 2 ottobre ($0.44 per 19 righe):
  - **mirato**, solo le righe `core-no-legs`, `football` e `pull-ups` con `--only`: circa $0.07;
  - **completo**, tutte le 20 righe, 1 ripetizione: circa $0.46, mezzo minuto a riga.

  Quale lancio?