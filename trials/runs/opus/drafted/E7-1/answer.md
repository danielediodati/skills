Ho aggiunto OpenRouter come terzo provider, ma non l'ho ancora provato con una chiamata vera: sono a pagamento e serve prima il tuo via libera.

**Cosa fa adesso:**
- `LLM_BACKEND=openrouter` e `ENTRANCE_BACKEND=openrouter` sono valori accettati.
- Si configura con `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` e `OPENROUTER_MAX_TOKENS`, che è opzionale: se è vuoto non mettiamo un tetto nostro ai token. Il modello di default è lo stesso di Groq (`qwen/qwen3.8-27b`), così cambiando provider non cambia anche il modello.
- Prima di ogni run, `ready()` chiede a OpenRouter la lista dei modelli. Il modello deve esserci e deve supportare `tools`; per planner e logger anche `structured_outputs`, perché devono produrre un documento con schema rigido. Se manca qualcosa, il messaggio dice quale variabile cambiare.
- Se i crediti OpenRouter sono finiti (errore 402), il run si ferma subito invece di riprovare, come già succede con la quota giornaliera di Groq.
- Ho aggiunto la dipendenza `langchain-openai`. Ho aggiornato anche `.env.example` e la tabella dei provider nel README.

**Le regole del charter del planner restano in piedi:**
- **Schema rigido:** con uno schema scritto come dizionario, `ChatOpenAI` non attiva la modalità `strict` (l'ho verificato: risulta `False`). Senza `strict`, l'elenco degli esercizi ammessi diventa un suggerimento. La nuova sottoclasse `ChatOpenRouter` la attiva, e le richieste vanno solo a provider che rispettano tutti i parametri inviati (`require_parameters`).
- **Nessuna regola spostata:** non ho toccato i charter né i prompt.

**Test e type check:**
- mypy è pulito.
- Su 1578 test ne passano 1575.
- I 3 che falliscono non dipendono da questa modifica. `tests/test_bot.py:2341` fissa `retest_date: "2026-10-15"`, che da oggi (19/10) è nel passato, quindi il validatore rifiuta l'esclusione. Non l'ho corretto perché è fuori da questa richiesta; basta una data calcolata rispetto a oggi.

**Cosa non ho potuto verificare:**
- Il controllo dei permessi ha bloccato l'esecuzione di `trainer plan` con un provider scelto da riga di comando. Il messaggio "manca la chiave" quindi è coperto dai test ma non l'ho visto stampato dal programma.
- Il percorso non ha mai fatto una chiamata reale a OpenRouter. Per verificarlo davvero serve un run di `trainer eval`: decidiamo prima insieme un budget di spesa.

**Da decidere tu:**
1. **Ragionamento "low":** il charter del planner, alla voce Budget, dice che `REASONING = "low"` vale per ogni modello che pianifica. Il percorso Groq già non lo applica e io ho fatto lo stesso per OpenRouter. Su OpenRouter si potrebbe passare `reasoning.effort`, ma con `require_parameters` un modello che non lo supporta non troverebbe più nessun provider. Dimmi se lo vuoi.
2. **Limite dei modelli gratuiti:** il limite giornaliero dei modelli `:free` restituisce un errore 429 di cui non conosco la forma esatta. Per ora viene trattato come un rifiuto qualsiasi, cioè si riprova fino a due volte.
3. **Variabili separate per planner e logger:** la ricerca proponeva `PLANNER_MODEL` e `LOGGER_MODEL`. Non le ho aggiunte, perché la richiesta era solo il provider.

Non c'è un repository git, quindi niente commit.