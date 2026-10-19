OpenRouter è ora il terzo provider: con `LLM_BACKEND=openrouter` (oppure `ENTRANCE_BACKEND=openrouter`) il coach usa OpenRouter. Non l'ho però mai provato contro OpenRouter vero: nessuna chiamata a pagamento, quindi niente spesa. Funziona per ora solo nei test locali, senza rete.

**Test:** mypy pulito. Suite: 1576 passati, 3 falliti. I 3 falliti sono in `tests/test_bot.py`, sulla conferma dell'esclusione, e non dipendono da questa modifica. Il fixture `proposing()` (`tests/test_logger.py:519`) ha la data di ritest fissa a `2026-10-15`, e il bot usa `date.today()`, cioè oggi 2026-10-19. Il validatore rifiuta quindi un'esclusione con ritest già passato. Lo deduco dal codice: il log del test non sono riuscito a stamparlo perché il comando mi è stato bloccato. Non l'ho corretto perché è fuori da questo lavoro; basta una data relativa a oggi.

**Charter:** ho letto quelli del planner e del logger. Il provider è configurazione, quindi nessuna linea si sposta. C'era però un rischio concreto per un vincolo:
- **Output strutturato:** l'integrazione OpenAI di LangChain manda `strict: false` quando chi chiama non passa `strict`. Planner e logger non lo passano, quindi l'enum degli id ammissibili sarebbe tornato un suggerimento. `ChatOpenRouter` in `coach/models.py` imposta `strict=True` di default per `json_schema`, e un test lo verifica.
- **Routing:** ogni richiesta porta `provider.require_parameters: true`. Così OpenRouter non la manda a un provider che ignorerebbe l'output strict.

**Cosa c'è:**
- **Variabili:** `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` (default `qwen/qwen3.8-27b`, lo stesso di Groq, così un confronto cambia solo il provider) e `OPENROUTER_MAX_TOKENS` (vuota = decide il modello).
- **Controllo prima del run:** se manca la chiave, la chiave è rifiutata, il modello non è servito o non supporta `tools` e `structured_outputs`, il problema viene mostrato prima di partire, con la riga da correggere. I suffissi come `:nitro` sono accettati.
- **Credito finito:** il 402 di OpenRouter è trattato come quota esaurita, quindi il run si ferma subito invece di riprovare.
- **Dipendenze:** aggiunte `langchain-openai` e `httpx`.
- **Documenti aggiornati:** `.env.example`, README e il punto 8 di ADR-0004.

**Cosa manca:**
- **Provider fissato:** la ricerca dice che un risultato di eval è riproducibile solo fissando il provider. Non l'ho fatto, perché va deciso quando si sceglie il modello.
- **Ragionamento:** su OpenRouter non viene chiesto un livello di ragionamento, come già succede su Groq.
- **Commit:** nessuno, perché la cartella non è un repository git.

Il primo run vero di `trainer plan` su OpenRouter consuma credito: decidiamo prima un budget?