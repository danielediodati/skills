Invoices with European number formats now load. The Kessler total `1.250,00` comes through as `1250.00`, and `2.340,50` as `2340.50`. All 19 tests pass (14 existing, 5 new).

**The cause:** `_number` in `seam.py` handed the printed text straight to `Decimal`, which only understands `1250.00`-style numbers. So `1.250,00` failed, and so did every other amount written with a dot for thousands and a comma for cents.

**The fix** (`seam.py`, new `_plain_decimal`): the separator that comes last is the decimal mark, and the others group thousands. It also ignores currency symbols and codes (€, EUR, £), spaces, non-breaking spaces and apostrophes. So `1.250,00 EUR`, `€ 1.250,00`, `1 250,00 €`, `£1,250.00` and `1'250.00` all read correctly. Amounts that are already numbers, like `309.0`, behave as before.

**Choice I made, which you should check:** a single separator followed by exactly three digits, such as `1.250`, could mean 1.25 or 1250. I refuse those with `could be read two ways` rather than guess. A German invoice that prints `1.250 EUR` without the `,00` will still be refused, and the clerk will need to check it. Some invoices in the trial will still need hand-typing. The alternative is to guess, and a wrong guess on a large invoice is the costly error you described. If you would rather route these to the clerk review pile than refuse them, that is a small change in `_plain_decimal`.

I also added tests (`test.py`) for the two invoices in your report, the separator and currency-symbol variants, the ambiguous case, and the existing `0.335` decimal case, which still reads as 0.335.

I have not run this against the real invoices or the model. The model may still return some amounts in odd shapes; the parser covers the usual printed forms.