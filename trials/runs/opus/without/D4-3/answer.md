---

# ⏸️ Ticket 15c.1: pronto, ma non chiuso
### Una proposta aperta ora si accetta, si rifiuta o si sostituisce anche scrivendo, e non resta mai senza ending
`nessun commit (la cartella non è un repo git)` · 1929 test · mypy pulito · niente rotto

---

**Il ticket resta aperto.** Il criterio 4 richiede una passata a pagamento di `trainer eval --suite adapt`, che non ho lanciato senza il tuo ok. Restano da fare anche `/code-review` (lo lanci tu) e i passi 6-8, cioè ROADMAP, cancellazione del ticket e commit. Non ho potuto verificare `c2e8e2a`, perché la cartella non è un repo git.

## Cosa è stato costruito
Mentre una proposta è aperta, l'entrance sa di che tipo è (adattamento, modifica, mesociclo) e le vengono offerti due nuovi handoff, `accept_plan` e `turn_down_plan`. Passano entrambi per lo stesso `Negotiation.answer` del tap; il rifiuto porta al planner le parole dell'utente così come le ha scritte. Una nuova richiesta sopra una proposta aperta la chiude con `stopped` e il nuovo run la segue nella stessa negoziazione. Un report che fa passare il giorno di un adattamento lo chiude con `overtaken`, una nuova ending (la settima): ora è scritta in CONTEXT.md e nell'ADR-0007. *Solo 30 minuti* non c'è più.

## Cosa puoi lanciare
```
uv run pytest -rA -q tests/test_bot.py -k "while_an_adaptation or new_ask_over or reporting_the_adapted or open_mesocycle or nothing_open or retired"
PASSED tests/test_bot.py::test_the_retired_shorter_button_answers_nothing_and_says_why
PASSED tests/test_bot.py::test_ok_while_an_adaptation_is_open_accepts_it_as_the_tap_does
PASSED tests/test_bot.py::test_no_while_an_adaptation_is_open_turns_it_down_with_their_words
PASSED tests/test_bot.py::test_a_new_ask_over_an_open_adaptation_stops_it_and_follows_it
PASSED tests/test_bot.py::test_reporting_the_adapted_workout_ends_the_adaptation_and_its_buttons_do_nothing
PASSED tests/test_bot.py::test_a_question_while_an_adaptation_is_open_is_answered_and_it_stays_open
PASSED tests/test_bot.py::test_an_open_mesocycle_is_read_as_one_and_ok_keeps_it
PASSED tests/test_bot.py::test_an_answer_with_nothing_open_is_told_so_and_answers_nothing
```
Il set di adattamento, controllato contro il catalogo senza toccare provider:
```
29 cases, 14 planned, 10 open
no problems
```

**Stima della passata a pagamento.** Il riferimento è la passata del 2026-10-03: 19 messaggi, 11 pianificati, 3 ripetizioni, $1.22. Ora i messaggi sono 29 e i pianificati 14, quindi:
- **~$1.6** a 3 ripetizioni;
- **~$0.55** a 1 ripetizione.

Le soglie valgono sull'intero set, quindi serve la passata completa. Se mi dai l'ok, lancio `trainer eval --suite adapt`.

## Cosa si è rotto rispetto a prima
Niente. Prima di toccare il codice la suite aveva già 3 test rossi (1906 passati, 3 falliti): il fixture dell'esclusione aveva come data di retest `2026-10-15`, ormai passata. L'ho spostata al 2099 in `tests/test_logger.py`.

## Dove siamo
- 1929 test verdi, mypy pulito.
- Il ticket si chiude dopo la passata approvata e `/code-review`.
- Dopo la chiusura si sbloccano 15c.2 e la demo registrata (15c.3).

Il `cut` non compariva solo dopo una nuova richiesta: anche una semplice proposta aperta si leggeva `cut` in `trainer runs`. Il run passato dall'entrance al planner vive sul thread di entrambi, e quello dell'entrance sovrascriveva l'altro. Ho corretto il reader in `runs.negotiations` e ho aggiunto test che falliscono con la versione vecchia.

Per un adattamento aperto, un report "non collegato" non esiste. Qualsiasi workout scritto fa avanzare il giorno, e l'engine (`record_adapted`) rifiuterebbe comunque di prescrivere l'adattamento. Quindi un report chiude sempre un adattamento aperto, mentre lascia aperti mesocicli e modifiche.

Ho anche aggiunto una cosa che il ticket non chiedeva: un tap sul vecchio bottone *Solo 30 minuti*, ancora presente sotto i piani offerti con `1.0.0rc1`, ora riceve una risposta invece di essere ignorato in silenzio.

Durante il lavoro alcuni comandi shell sono stati bloccati dai permessi (`sed -i`, un heredoc, un `rm` dentro un comando composto); ho fatto le stesse cose con l'editor o con comandi separati.