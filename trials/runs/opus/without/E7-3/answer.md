OpenRouter ora è un terzo provider: `LLM_BACKEND=openrouter` oppure `ENTRANCE_BACKEND=openrouter`. Però nessun piano vero è passato da OpenRouter, perché non c'è una chiave reale.

## Cosa è stato costruito
- **Il backend** in `src/trainer/coach/models.py` usa il pacchetto `langchain-openrouter`. Servono `OPENROUTER_API_KEY` e `OPENROUTER_MODEL`. Il modello predefinito è `qwen/qwen3.8-27b`, lo stesso di Groq: cambiando solo il provider il modello resta lo stesso nel confronto.
- **Lo schema strict resta garantito.** I grafi chiedono l'output strutturato senza `strict`, e il pacchetto in quel caso non lo manda. Ho fatto una sottoclasse che lo attiva sempre. In più OpenRouter manda le richieste solo ai provider che rispettano tutti i parametri (`require_parameters`). Senza queste due cose, l'elenco degli id di esercizio ammessi tornerebbe a essere solo un suggerimento.
- **Controlli prima che il run parta**, segnalati come stati:
  - chiave mancante;
  - chiave rifiutata (401);
  - modello che OpenRouter non serve: il suffisso `:nitro` è accettato;
  - credito finito (402): diventa `QuotaSpent`, così il planner non lo ritenta come un turno qualsiasi.
- **Documenti aggiornati:** `.env.example`, la tabella dei provider nel README, il punto 8 di ADR-0004 e la docstring di `trainer bot`.

## Cosa ho verificato
- **Test:** 1574 passano e 3 falliscono. Sono gli stessi 3 di prima della modifica (`test_bot.py`, i bottoni di esclusione, che non c'entrano con i provider). Dei test nuovi, 12 passano.
- **mypy:** pulito.
- **Contro OpenRouter vero, con una chiave finta:**
  ```
  state: OpenRouter refuses the key in OPENROUTER_API_KEY (User not found.); make one at https://openrouter.ai/settings/keys
  ```
  La lista dei modelli risponde (470 modelli), e contiene sia lo slug predefinito sia `anthropic/claude-sonnet-5`.

## Cosa non ho potuto verificare
- **`trainer plan` dalla CLI:** il comando è stato negato perché questa sessione non può approvare permessi. L'ho provato solo da Python.
- **Un piano reale:** senza chiave non so se la modalità strict regga davvero con i provider scelti da OpenRouter. Il primo test da fare con la tua chiave, con `TRAINER_DB` puntato sulla fixture:
  ```
  LLM_BACKEND=openrouter uv run trainer eval --suite plan
  ```

## Cosa si è rotto rispetto a prima
Niente nei test. C'è però un effetto collaterale: l'SDK `openrouter` richiede `pydantic<2.13`, quindi pydantic è sceso da 2.13.5 a 2.12.5. Su Python 3.14 questo fa comparire un `UserWarning` a ogni avvio. Se ti dà fastidio, si può usare `ChatOpenAI` con il `base_url` di OpenRouter, che non ha questo vincolo.

La cartella non è un repository git, quindi non ho fatto nessun commit.