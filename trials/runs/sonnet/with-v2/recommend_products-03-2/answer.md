I haven't changed anything, because this fix needs a line in the charter moved, and only you can do that.

**The line:** `evals/recommend_products/charter.md` lists "What each reason says" as a free model decision, and it states "claims in it are not checked". Code that scans the reason for prices and blanks it when one differs from the catalogue price is a check on those claims. That would also make the reason partly code-decided, which the charter doesn't allow.

**What moving it would buy:** a guarantee that no strip goes out with a wrong price in the reason. Since the charter already keeps an empty reason ("the right product without a reason beats no product"), your requirement to show the product without a reason fits the existing design. The check itself would be small:

- Find currency-like numbers in the reason, such as `€14.90`, `$4`, `19,90` or `14.90 EUR`.
- Compare each to the product's catalogue price.
- Set `reason` to `""` if any differs.
- Leave other numbers alone ("2 m", "30-hour"), which the pattern would have to be tuned to avoid flagging.

**What I did not do:** I did not add a prompt instruction like "never mention prices". It would only lower the rate of wrong prices without guaranteeing none, and it would take away part of what the charter leaves to the model.

**Your decision:** if you want the check, update the charter. For example, change the "What each reason says" line to say that claims aren't checked except that a stated price must match the catalogue, and add a matching Constrained entry. Then I'll implement it in `seam.py` with tests for the cases you gave (19.90 vs 14.90, the $4 cable, a correct 19.90, and "2 m" / "30-hour battery").