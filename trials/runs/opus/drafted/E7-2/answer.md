## OpenRouter aggiunto come provider (non verificato con chiamate reali)

`LLM_BACKEND=openrouter` e `ENTRANCE_BACKEND=openrouter` adesso funzionano. Non ho fatto nessuna chiamata a OpenRouter, quindi nessuna spesa: tutto quello che segue è verificato solo dai test offline.

**Test:** 1578 passati e 3 falliti. mypy è pulito su 85 file. I 3 fallimenti non dipendono da questa modifica (spiegazione in fondo).

### Cosa è stato costruito
- **Il backend.** Il nuovo backend sta in `coach/models.py`. Passa dall'API compatibile OpenAI di OpenRouter, tramite il pacchetto `langchain-openai`. Si configura con `OPENROUTER_API_KEY` e `OPENROUTER_MODEL`. Il modello di default è lo stesso di Groq (`qwen/qwen3.8-27b`), così cambiando provider il modello resta quello.
- **Le regole delle charter restano in codice, nessuna linea spostata:**
  - **Schema strict.** `ChatOpenAI` di suo manda gli schemi dict *non* strict, e così l'enum degli id ammissibili diventerebbe solo un suggerimento. L'ho forzato a strict. Ho rotto apposta la correzione e il test è fallito, quindi il test la protegge davvero.
  - **Reasoning.** Il planner e il logger ricevono `reasoning: low`, l'entrance no.
  - **Provider affidabili.** Con `require_parameters: true` OpenRouter non smista mai la richiesta verso un provider che ignorerebbe in silenzio lo schema, i tool o il reasoning.
  - **Quota esaurita.** Il credito finito (errore 402) e il limite giornaliero dei modelli gratuiti fermano subito la run (`QuotaSpent`). Il limite al minuto invece non la ferma.
- **Controlli prima della run.** `ready()` controlla la chiave, poi che OpenRouter offra quel modello, poi che il modello supporti quello che serve al nodo: tool per l'entrance, più structured outputs e reasoning per il planner. Così un modello inadatto viene segnalato prima di partire, invece di dare un 404 a metà run.
- **Documentazione aggiornata:** `.env.example`, README, ADR-0004 punto 8 e la docstring di `trainer bot`.

### Cosa si è rotto rispetto a prima
Niente per colpa di questa modifica. I 3 test di `test_bot.py` sull'esclusione falliscono per un problema di date già presente. `proposing()` in `tests/test_logger.py:519` ha la data di retest fissata a `2026-10-15`, e quei test usano la data vera (oggi è il 19/10). Il validator quindi rifiuta la data perché "non è dopo oggi". Non l'ho corretto perché non c'entra con OpenRouter, ma la correzione è di una riga: la data relativa a oggi. Vuoi che la faccia?

### Cosa non ho potuto fare
- **Prova della CLI.** I comandi `python -c` e `trainer …` sono stati bloccati dai permessi, e comunque non potevo lanciare `trainer eval` per evitare di toccare una chiave reale in `.env`.
- **Commit.** La cartella non è un repo git, quindi non c'è nessun commit.
- **Dipendenze.** Ho aggiunto `langchain-openai` e `httpx` a `pyproject.toml`. `uv add` ha anche aggiornato `langchain-core` da 1.6.3 a 1.6.12.

### Prossimi passi (servono la tua approvazione e un budget)
1. **Una prova reale:** una `trainer plan` su OpenRouter. Costa pochi centesimi, ma va concordato un budget prima.
2. **Fissare il provider dentro OpenRouter**, ad esempio con `OPENROUTER_PROVIDER`. Lo studio lo raccomanda perché i risultati delle eval siano riproducibili.
3. **Un modello per ogni nodo** (`PLANNER_MODEL`, `LOGGER_MODEL`), come suggerisce lo studio.