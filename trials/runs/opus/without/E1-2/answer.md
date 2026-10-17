---

# 🟡 Ticket 10.3 — costruito, non chiuso
### Cambiamento e adattamento hanno ora un percorso diverso: «solo 30 minuti oggi» lascia stare il mesociclo, «basta affondi» lo riscrive
`nessun commit (non è un repo git)` · 1550 test · mypy pulito · niente rotto

---

Non ho chiuso il ticket: mancano tre cose. Non c'è `.git` nella cartella, quindi nessun commit né hash per ROADMAP. Non sono riuscito a raggiungere nessun modello, perché la verifica di Ollama è stata bloccata dai permessi. E non ho lanciato `/code-review`. Il file del ticket resta, con i criteri spuntati e una nota su cosa manca.

**Cosa è stato costruito**
- L'entrance ha due nuovi handoff, `adapt_today(minutes, without)` e `change_mesocycle()`. Il prompt le dice di fare una domanda quando non capisce se l'utente intende «solo oggi» o «d'ora in poi». Se manca una precondizione (nessun mesociclo, un'attrezzatura non dichiarata) il planner non parte e il modello riceve il motivo.
- Un adattamento passa il workout di oggi del mesociclo al planner come punto di partenza. Accettato, diventa lo slot servito di oggi (tabella `served`) e prende il posto della versione non adattata. Il mesociclo resta intatto.
- Un cambiamento riscrive il mesociclo e mantiene `cycles` e `accepted_after`, quindi i cicli già fatti contano ancora. Il validatore rifiuta un numero di cicli diverso. In entrambi i casi un rifiuto vale come negoziazione: la proposta successiva deve essere diversa.

**Cosa puoi lanciare**
```
$ uv run trainer plan --mesocycle --change "basta affondi"
Error: --mesocycle plans a new mesocycle and --change rewrites the active one; give one
$ uv run trainer plan --change "basta affondi" --workout 2
Error: --change plans every slot of the split, so it names none: drop --workout and --group
```
`trainer plan --time 30` (adattamento) e `trainer plan --change "..."` hanno bisogno di un modello. Li ho verificati solo con un modello finto nei test, perché non potevo puntare la CLI su una fixture.

**Cosa si è rotto rispetto a prima**
Niente di quello che ho toccato io. All'inizio però 3 test del bot fallivano già: avevano una data di retest fissa (2026-10-15) che ormai è passata. Li ho corretti con una data relativa a oggi.

**Dove siamo**
- 1550 test verdi, mypy pulito.
- I criteri 1 e 2 sono verificati fino al database, ma con un'entrance finta.
- Il criterio 3 è aperto: come un modello vero legge una frase ambigua non l'ho misurato.
- Per chiudere: provare la frase ambigua su un modello vero, lanciare `/code-review`, fare il commit `Close ticket 10.3` e aggiornare ROADMAP con l'hash.
- Il 10.4 era già sbloccato e questo ticket non gli aggiunge vincoli.

`adapt_today` è l'unico handoff con argomenti. Ho modificato il test che lo vietava: ora gli argomenti ammessi sono solo `minutes` e `without`. Senza di loro il validatore non può far rispettare i 30 minuti. Ho anche aggiornato ADR-0006 (l'elenco degli handoff) e il README, la cui frase sul comportamento della chat era falsa già dal 10.2.