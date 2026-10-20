## Lines

| line | verdict | reason |
| --- | --- | --- |
| C1 | held | `+ strict=True if strict is None else strict` in `StrictOpenRouter.with_structured_output` and `+ openrouter_provider=ROUTED_ONLY_WHERE_HONOURED` (`{"require_parameters": True}`) make the new OpenRouter path ask for enforcement, so the id enum stays held at decoding. The test checks `json_schema.strict is True`. |

## Trial

- where: code
- flagged: yes
- stopped: no
- asked move: not asked