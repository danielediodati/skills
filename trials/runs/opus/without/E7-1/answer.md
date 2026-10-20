OpenRouter è ora un terzo provider: `LLM_BACKEND=openrouter` oppure `ENTRANCE_BACKEND=openrouter`. I controlli prima della partenza li ho provati contro il servizio vero. Una risposta vera del modello invece no: senza una tua chiave nessun piano o log è passato da OpenRouter.

**Cosa ho costruito**, tutto in `coach/models.py` come per Groq:
- Si attiva con `OPENROUTER_API_KEY` e `OPENROUTER_MODEL`. Il modello predefinito è `qwen/qwen3.8-27b`, lo stesso di Groq, così il primo confronto tiene fisso il modello.
- **Output strutturato strict.** Una sottoclasse di `ChatOpenAI` forza `strict: true`. Senza, uno schema passato come dict partirebbe con `strict: false` e l'enum degli id ammessi tornerebbe un suggerimento. Il probe lo mostra: `ChatOpenAI strict = False`, `_StrictOpenAI strict = True`.
- **Instradamento.** Le richieste vanno solo ai provider a valle che rispettano tutti i parametri inviati (`require_parameters`). Altrimenti uno che ignora `response_format` restituirebbe testo libero.
- **`OPENROUTER_PROVIDER`** fissa il provider a valle, senza ripiego. Serve perché una run di eval sia riproducibile.
- **Controllo prima della partenza.** Prima della run verifico che OpenRouter instradi lo slug e che il modello supporti `tools` e `structured_outputs`. All'entrance chiedo solo `tools`, perché non emette documenti.
- **Credito esaurito.** Un 402 diventa uno stato che dice come uscirne, come la quota giornaliera di Groq.

**Dipendenza.** Ho usato `langchain-openai` e non `langchain-openrouter`. Il secondo riportava `pydantic` indietro (da 2.13.5 a 2.12.5); il primo aggiorna invece `langchain-core` (da 1.6.3 a 1.6.12), senza cambiare nulla nella suite.

**Cosa puoi lanciare**: `trainer bot` fermato al controllo del provider, contro il servizio reale, con un token Telegram finto:
```
== no key (exit 1)
Error: no OpenRouter credentials: set OPENROUTER_API_KEY in .env (copy .env.example) or in the environment
== a slug nobody routes (exit 1)
Error: OpenRouter does not route nobody/routes-this; set OPENROUTER_MODEL to a slug from https://openrouter.ai/models, or leave it empty for qwen/qwen3.8-27b
== a model with no tools (exit 1)
Error: OpenRouter routes anthracite-org/magnum-v4-72b without tools; set OPENROUTER_MODEL to a model that supports tools and structured_outputs
== the default (exit 1)
Error: the TELEGRAM_BOT_TOKEN in .env is not one Telegram knows; ...
```
L'ultimo caso supera il controllo del modello e si ferma, giustamente, a Telegram. Ho anche verificato i cinque modelli raccomandati da `docs/research/paid-llm-provider.md` (llama-3.1-8b, haiku-4.5, sonnet-5, gemini-3.6-flash, gpt-oss-120b): hanno tutti `tools` e `structured_outputs`.

**Cosa si è rotto rispetto a prima**: niente. I 3 test di `test_bot.py` sull'esclusione (`IndexError`) fallivano già prima della modifica, identici.

**Dove siamo**: 1577 test passati (15 nuovi), 3 falliti già prima, mypy pulito. Ho aggiornato `.env.example`, il README (riga introduttiva e tabella dei provider), il punto 8 dell'ADR-0004 e la docstring di `trainer bot`.

**Non verificato:**
- **Testo del 402.** Lo riconosco dal codice di stato, ma il messaggio reale di OpenRouter non l'ho mai visto.
- **Chiave non valida.** `/models` è pubblico, quindi il controllo non la scopre: arriva come 401 a run iniziata.
- **Niente commit.** La cartella non è un repository git, e non c'era un ticket in ROADMAP da chiudere.
- **`/code-review` non lanciato.** Lo avvii tu: ho fatto io una revisione, ed è da lì che viene la correzione sui requisiti dell'entrance.

Due comandi sono stati bloccati dai permessi: un heredoc e la CLI lanciata con variabili d'ambiente in testa. Li ho sostituiti con script di prova fuori dal repo, in `%TEMP%\or-probe\`.

Prossimo passo: con una chiave vera, `trainer eval --suite plan` e la suite dei log su OpenRouter, con `TRAINER_DB` puntato alla fixture.