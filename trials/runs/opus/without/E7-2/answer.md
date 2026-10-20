Ho aggiunto OpenRouter come terzo provider con `LLM_BACKEND=openrouter`. Il test suite non è tutto verde: 1575 passati e 3 falliti, che non dipendono da questa modifica (spiego sotto). mypy è pulito. Non c'è niente di committato, perché la cartella non è un repository git.

**Cosa ho costruito**
- In `coach/models.py` il backend segue lo stesso schema di Groq:
  - Usa il pacchetto `langchain-openrouter` (0.2.9), che ho aggiunto come dipendenza.
  - Le nuove variabili sono `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` e `OPENROUTER_MAX_TOKENS`.
  - Se manca la chiave, il bot si ferma e dice di impostarla in `.env`.
  - Prima del run controlla che OpenRouter abbia il modello indicato. Se non ce l'ha, l'errore nomina la variabile da correggere: `OPENROUTER_MODEL` o `ENTRANCE_MODEL`.
- **Modello di default:** `qwen/qwen3.8-27b`, lo stesso di Groq, così cambiando provider non cambia altro. Per provare un modello di frontiera basta una riga, per esempio `OPENROUTER_MODEL=anthropic/claude-sonnet-5`.
- **Instradamento:** le richieste vanno solo ai server che rispettano lo schema JSON e i tool (`require_parameters: True`). Altrimenti uno di quei server potrebbe ignorare lo schema rigido, e con esso il vincolo sugli esercizi ammessi.
- **Limite di token:** `OPENROUTER_MAX_TOKENS` non ha valore di default. Il tetto di 1000 di Groq serve solo per il piano gratuito di Groq.
- Funziona anche solo per l'entrance: `ENTRANCE_BACKEND=openrouter`.
- Ho aggiornato `.env.example` (la sezione OpenRouter diceva ancora «not read yet»), il README e il punto 8 dell'ADR-0004. Ho anche aggiunto `openrouter` al test che vieta a `engine/` di importare SDK dei modelli.

**Cosa ho verificato**
- 16 nuovi test passano (14 in `test_models.py`, 2 in `test_cli.py`), tra cui:
  - `trainer bot` senza chiave si ferma con `OPENROUTER_API_KEY`;
  - con la chiave parte con `provider:    openrouter` e non chiede niente a Ollama.
- Il vero `ChatOpenRouter` si costruisce e accetta sia `bind_tools` sia `with_structured_output(method="json_schema")`, cioè le due chiamate che usano planner e logger.
- L'endpoint pubblico `/api/v1/models` risponde 200 con 470 modelli, compresi `qwen/qwen3.8-27b` e `anthropic/claude-sonnet-5`.

**Cosa non ho potuto verificare**
- Non ho mai lanciato `trainer plan` su OpenRouter. In questa sessione non posso eseguire comandi con variabili d'ambiente, e comunque non c'è una chiave vera. Sul piano e sul logger reali non ho ancora numeri.
- Quando la quota finisce o il credito è esaurito (errori 429 o 402), OpenRouter non riceve un messaggio chiaro come Groq con `spent()`. Non conosco il testo esatto di quegli errori senza una chiave, quindi per ora arrivano come errori normali del provider.

**I 3 test falliti in `test_bot.py`** riguardano le esclusioni proposte e non c'entrano con OpenRouter. In `tests/test_logger.py:519` la funzione `proposing()` usa come data di retest `2026-10-15`, fissa nel codice. Oggi è il 17 ottobre, e `log.py:732` rifiuta un retest uguale o precedente a oggi. Sono partiti a fallire da soli col passare dei giorni. Li ho visti fallire anche col pydantic di prima, ma senza git non ho una baseline per confermarlo con un run. La correzione è calcolare la data a partire da oggi, ma non l'ho toccata perché è fuori da questa richiesta: dimmi se la sistemo.