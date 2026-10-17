Ho scritto la bozza del documento di metodologia in `src/trainer/data/methodology.md`, pronta per le tue modifiche. Il ticket 11.2 non è chiuso: resta `needs-info` finché non l'hai rivista.

**Cosa contiene**, una sezione per ciascuna delle quattro domande del ticket:

| § | domanda | proposta |
|---|---|---|
| 1 | cos'è un working set | 1-3 ripetizioni dal cedimento, 6-15 reps, 3-4 giri. Un giro solo è riscaldamento. Se superi ~20 reps facili, passi a una variante più difficile (lungo `regression_of` / `variant_of`) invece di aggiungerne una seconda |
| 2 | quanti esercizi per gruppo | i minuti assegnati al gruppo ÷ 8, minimo 1 e massimo 3. Due esercizi dello stesso gruppo devono differire per pattern o angolo |
| 3 | che recupero per quale intento | una tabella per intento: forza, ipertrofia sui multiarticolari, isolamento, superset, circuito |
| 4 | quando superset o circuito | superset solo tra muscoli primari che non si sovrappongono (antagonisti). Circuito per riscaldamento, core, condizionamento o allenamenti da 20 minuti o meno. Mai varianti dello stesso movimento |
| 5–6 | ordine e caso di prova | il circuito da 25 minuti della sessione 7 accanto a un piano da ~37 minuti più setup, calcolato con la formula dell'engine |

**Cosa devi decidere tu.** Sono marcate **Decide** nel file:
- il target di ripetizioni dal cedimento, e se il piano debba riportarlo (oggi lo schema non ha un campo per farlo);
- il volume per muscolo per ciclo: la letteratura ragiona a settimana, REPS a ciclo;
- la fascia di recupero per l'ipertrofia: TRAINER.md dice 90-120 s, la fonte [2] suggerisce di più. Se la allarghi, va corretto anche TRAINER.md;
- il riscaldamento: ADR-0002 vieta le serie di avvicinamento sullo stesso esercizio.

**Da sapere prima di modificarla:**
- **Le fonti le ho citate a memoria.** Sono articoli reali per quanto ne so, ma volumi e pagine vanno controllati. Il file lo dice esplicitamente.
- **Non segue l'ordine della roadmap.** La 11.1, la misura che distingue le cause, non è ancora fatta. C'è però un indizio a favore del "brief vuoto": il commento nel 11.3 riporta che `gpt-oss-120b` su OpenRouter ha prodotto la stessa forma di piano.
- **La posizione del file è una mia scelta.** L'ho messo accanto a `muscle-groups.md` perché un file letto dal planner deve stare nel pacchetto. Spostarlo costa poco.
- **Il planner non lo legge ancora.** Il documento va nel brief, non nel validator. Se vuoi che qualche regola diventi un controllo dell'engine (per esempio "nessun muscolo primario due volte in un blocco"), bisogna riaprire ADR-0001.
- **Ho aggiunto un commento al ticket** con lo stato della bozza e i passi successivi: collegarla a `PLANNING` e `MESOCYCLE_PLANNING`, e giudicare i piani con una soglia dichiarata come in ADR-0010.
- **Niente commit.** La directory non è un repository git (`fatal: not a git repository`), quindi non ho trovato `a9b2c50`.
- **Un comando è stato bloccato** per mancanza di approvazione: una `grep` per leggere `duration.py`. Ho letto lo stesso file con lo strumento di lettura, quindi non manca nulla.