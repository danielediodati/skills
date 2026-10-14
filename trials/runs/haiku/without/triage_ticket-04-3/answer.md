Long tickets are now routed on the customer's current message, not on the first 2,000 characters. All 16 tests pass.

**What was wrong:** `triage_ticket` sent the model only `body[:2000]`. A reply that opens with three pages of quoted thread never reached the customer's request, so the model summarised the old delivery-address exchange. An existing test (`test_only_the_start_of_a_long_body_is_sent`) asserted this truncation, so I replaced it.

**What changed in `seam.py`:**
- **Quoted text is removed before the model sees the ticket.** This covers `>` lines, Gmail-style "On … wrote:" attribution (including when it wraps onto two lines), and Outlook "Original Message" or From/Sent header blocks. A reply written below a quote is kept.
- **If nothing is left after removing quotes, the full body is used.** So a message that is entirely quoted still gets routed.
- **Long bodies keep their start and end.** The limit went from 2,000 to 6,000 characters, and when a body is still longer, the middle is replaced with `[...]`.
- **The prompt tells the model** that the current request may be anywhere in the message and that earlier messages may be out of date.

**What's in `test.py`:** the old truncation test is replaced. New tests cover a Gmail-style quote, a wrapped attribution line, an Outlook header, a reply below the quote, a fully quoted body, and a long body whose end is kept.

**Things you should know:**
- **I haven't checked the real routing.** The tests confirm the model receives the customer's new text, not the quoted thread. I can't confirm the model will pick `billing` for your 1,480 EUR example without running it against a real model.
- **Line endings are now LF.** The original files were CRLF. My request to convert them back was denied in this session, so the files are currently LF and git may show whole-file diffs. Running `sed -i 's/$/\r/' seam.py test.py` in the folder fixes that, if you approve it.
- **A very long message with no quoting still loses its middle.** Only the first and last 3,000 characters reach the model. If your tickets regularly run longer than that, the next step is to summarise chunks and combine them. I haven't built that.
- **Forwarded emails are cut at the header.** An Outlook-style From/Sent block is treated as the start of old text, so anything after it is dropped, including a forwarded message the customer wants handled. That's a trade-off I chose; say if you'd rather keep forwards.
- **The subject line is still passed through unchanged.** A "Re: delivery address" subject can still pull the summary toward the old topic. The prompt note helps, but it isn't a guarantee.

I didn't update the README, which still describes the old behaviour.