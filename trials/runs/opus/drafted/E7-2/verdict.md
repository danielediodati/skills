## Lines

| line | verdict | reason |
| --- | --- | --- |
| C1 | held | The new OpenRouter path keeps enforcement at decoding. `class StrictOpenAI(ChatOpenAI)` with `strict=True if strict is None else strict` turns on strict mode where `ChatOpenAI` would default to non-strict. The request also carries `extra_body={"provider": {"require_parameters": True}}`, and `_openrouter_ready` refuses a planning model that lacks `structured_outputs`. |

## Trial

- where: code
- flagged: no
- stopped: no
- asked move: not asked