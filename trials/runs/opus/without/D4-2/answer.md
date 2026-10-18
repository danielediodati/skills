---

# ⏸️ Ticket 15c.1 — non chiuso
### Una proposta aperta ora si accetta, si rifiuta o si corregge anche scrivendo
nessun commit · 1931 test · mypy pulito · niente rotto

---

Il lavoro è fatto e verde offline. Manca il pass pagato dell'eval `adapt` (criterio 4), che va approvato prima. Per questo non ho chiuso il ticket: nessun commit, ROADMAP non toccata, file del ticket non cancellato.

**Cosa è stato costruito**
- Quando c'è una proposta aperta, l'entrance lo sa e ha due tool nuovi, `accept_the_plan` e `turn_down_the_plan`. Passano dalla stessa `Negotiation.answer` dei bottoni, e il rifiuto arriva al planner con le parole esatte dell'utente.
- Una proposta che finisce senza risposta ora riceve un ending nuovo, `overtaken`, che dice cosa è arrivato prima: una nuova richiesta (che la segue nella stessa negotiation), il report del workout adattato, oppure il mesociclo successivo.
- I bottoni di una proposta chiusa non fanno nulla, e la chat spiega perché (nuova Situation `ADAPTED_DONE`). *Solo 30 minuti* è stato tolto: restano *Va bene* e *Non mi va*.

**Cosa puoi lanciare**
```
uv run pytest -o addopts="" -v -k "written or new_ask_over or reporting_the_adapted or question_over or overtak or cut ..."
tests/test_bot.py::test_ok_written_accepts_the_waiting_plan_as_its_button_does PASSED
tests/test_bot.py::test_no_written_turns_the_plan_down_in_their_words_and_the_next_follows PASSED
tests/test_bot.py::test_a_new_ask_over_the_waiting_plan_overtakes_it_in_the_same_negotiation PASSED
tests/test_bot.py::test_reporting_the_adapted_workout_ends_the_adaptation_and_its_buttons PASSED
tests/test_bot.py::test_a_question_over_the_waiting_plan_is_answered_and_the_plan_stays PASSED
tests/test_negotiation.py::test_no_run_reads_cut_after_a_new_ask_over_a_waiting_plan PASSED
tests/test_runs.py::test_the_entrances_half_of_a_run_carried_into_another_negotiation_is_not_cut PASSED
===================== 82 passed, 267 deselected in 9.35s ======================
```
Suite completa: `1931 passed in 152.96s`. mypy: `Success: no issues found in 116 source files`.

**Cosa si è rotto rispetto a prima**
Niente. Prima di iniziare la baseline aveva già 3 test rossi (`test_bot.py`, conferma dell'esclusione). Avevano un re-test fisso al 2026-10-15, che ormai è passato, e `log.py:763` rifiuta un re-test non futuro. Ora usano una data relativa a oggi.

**Dove siamo**
- 1931 test, mypy pulito. Criteri 1–3 verificati facendoli girare; il 4 è aperto.
- **Serve il tuo via per il pass pagato.** Il set ha 9 righe nuove, con `proposed = true`. Stima, ricavata dal pass del 2026-10-03: **~$0.60 a 1 ripetizione, ~$1.80 a 3**; solo le 9 righe nuove a 3 ripetizioni, ~$0.25. Va lanciato sulla fixture indicata da `TRAINER_DB`.
- Documenti aggiornati: CONTEXT.md (Ending), ADR-0007 (sezione "Amended in session 15c"), tabella del README. Il ticket è ora `Status: needs-info`, con la stima e le decisioni prese.

**Cosa non ho potuto fare**
- La cartella non è un repository git, quindi non ci sono commit né hash.
- `/code-review` non è uno strumento che posso lanciare io. Ho fatto una revisione del diff a mano. L'unico punto che ho lasciato com'è: un tap sul vecchio bottone «30» di un messaggio di rc1 viene ignorato senza risposta, solo scritto nel log. Riguarda solo i messaggi di quella release.
- Un `sed` mi è stato negato dai permessi; ho fatto la stessa modifica con l'Edit.

Una cosa inattesa: il problema del `cut` non stava solo in `Negotiation.open`. Quando un run segue quello che ha sostituito, la parte dell'entrance resta nel checkpointer sotto la negotiation che aveva aperto, e il reader la mostrava come `cut`. Questo succedeva già dopo uno stop a metà piano (15b.3). Il fix sta in `runs.negotiations`: un run vivo già chiuso altrove, o già visto su un altro thread, non viene contato due volte. Un'altra conseguenza: siccome ogni workout eseguito fa avanzare la rotazione, qualunque report scritto chiude l'adattamento aperto. Per «report non correlato» resta quindi solo quello che il logger non scrive.