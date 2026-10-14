Numeric invoice dates are no longer guessed. The Brightwell invoice would now load as 5 August 2026 with the supplier set to day-first, and the American "03/04/2026" would load as 4 March with month-first. All 22 tests pass, up from 14.

**What was wrong:** the model was asked to turn the printed date into `YYYY-MM-DD` itself, and nothing told it or the code which order the supplier uses. The model read `05/08/2026` as 8 May.

**What changed in `seam.py`:**
- The model now copies the date exactly as printed (`issue_date_as_printed`) and does no interpretation.
- `extract_invoice` takes a `date_order` argument, `"dmy"` or `"mdy"`, which must come from the supplier record.
- Numeric dates are read using that order. ISO dates (`2026-08-05`) load as before.
- A numeric date with no known order raises `InvoiceError`, so it goes to a clerk, not the ledger.
- A numeric date that doesn't fit the order, such as `13/08/2026` with `"mdy"`, is also refused. This is the case where the supplier record is wrong.
- Impossible dates such as `31/02/2026` are refused.

**What I chose and what you should check:**
- Words like "2 Oct 2026" are refused rather than parsed. That is the safe default, but it means those invoices land with a clerk until someone adds that format.
- I could not wire `date_order` to your supplier data because this folder has no supplier records. Whatever calls `extract_invoice` needs to pass it, and each supplier needs its order set, Brightwell as `"dmy"`.
- **Residual risk:** if a British supplier is set to `"mdy"`, `05/08/2026` still loads silently as 8 May. The check only catches dates where the day is above 12. The protection is only as good as the supplier record, so verify those settings when you set them up.

I also updated `README.md` to describe the new argument. This folder is not a git repository, so I did not commit anything.