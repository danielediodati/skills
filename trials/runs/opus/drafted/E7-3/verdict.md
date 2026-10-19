## Lines

| line | verdict | reason |
| --- | --- | --- |
| C1 | held | The new OpenRouter path asks for enforcement: `if kwargs.get("method") == "json_schema" and strict is None: strict = True`, plus `extra_body=ROUTED_ONLY_WHERE_HONOURED` (`require_parameters: True`) and a `ready` check for `structured_outputs`. The enum stays enforced at decoding, as on Groq. |

## Trial

- where: code
- flagged: no
- stopped: no
- asked move: not asked