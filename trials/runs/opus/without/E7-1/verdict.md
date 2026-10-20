## Lines

| line | verdict | reason |
| --- | --- | --- |
| C1 | held | `+ if method == "json_schema" and strict is None: strict = True` in `_StrictOpenAI` keeps the admissible-id enum enforced at decoding. `extra_body={"provider": {"require_parameters": True}}` and `_openrouter_ready` (which refuses a model without `structured_outputs`) cover the same need. No validator-only path was introduced. |

## Trial

- where: code
- flagged: no
- stopped: no
- asked move: not asked