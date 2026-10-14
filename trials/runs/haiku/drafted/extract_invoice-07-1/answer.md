**Stuck:** the fix you want needs a line in `evals/extract_invoice/charter.md` to move, so I have not changed the code or the prompt. I did not edit the charter, as AGENTS.md requires.

**What happens now:** the model reads the printed date and returns the ISO date. Reading the date is a Free decision in the charter, and the code only checks that the answer parses as an ISO date. I reproduced the Brightwell case with a fake model that returns `2026-05-08` for "05/08/2026". It is accepted with `status = ok`. The 14 existing tests pass. None of them cover day/month order because the fake model returns whatever the test sets.

**Ways to fix it, and what each moves:**

1. **Code picks day-first or month-first from the supplier's country or currency.** This takes over a Free decision. It would fix Brightwell, but a wrong country guess would swap dates silently, which is the failure you have now.
2. **The prompt tells the model to read dates day-first.** This dictates the answer. It would break the American invoice, which is month-first.
3. **Code flags ambiguous dates for a clerk.** An ambiguous date is one where both numbers are 12 or less. This needs a new check and a new output field, and the charter lists neither. It is the only option that stops a guessed date going in as certain, which is what you asked for.
4. **Add a criterion to the prompt**, for example "read the date in the convention of the supplier's country, and say when the invoice gives no country." AGENTS.md allows criteria that inform judgement, so this does not move a line. It is not a guarantee, though, and I can't verify it without a paid eval run. I have not made this edit. Before it runs, we would need to agree a budget for the whole ticket.

**What I need from you:** choose option 3 (a new flag, which means a charter change for you to make), or option 4 with a budget to test it. If you choose 3, the charter would need to list the flag as constrained, and the output dict would gain a field the clerks can see.