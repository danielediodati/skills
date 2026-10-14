## Lines

| line | verdict | reason |
| --- | --- | --- |
| F1 | held | not touched |
| F2 | moved toward code | `+ day, month = (first, second) if date_order == "dmy" else (second, first)`, and the prompt now asks for `issue_date_as_printed`: code reads an ambiguous date from a caller-supplied order where the line leaves it to the model. |
| F3 | held | not touched |
| F4 | held | not touched |
| F5 | held | not touched |
| F6 | held | not touched |
| F7 | held | not touched |
| F8 | held | not touched |
| C1 | held | The code still raises `InvoiceError` for a bad `issue_date`, and it builds the `date` itself from the printed text. |
| C2 | held | not touched; still only `re.fullmatch(r"[A-Z]{3}", currency)`, so the gap is unchanged. |
| C3 | held | not touched; the total is still the amount due and the gap is unchanged. |
| C4 | held | not touched |
| C5 | held | not touched |
| C6 | held | not touched; still one `model(...)` call. |
| C7 | held | not touched |
| B1 | held | not touched |

## Trial

- where: both
- flagged: no
- stopped: no