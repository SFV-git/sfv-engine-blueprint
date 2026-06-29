# RESULT -- BLUEPRINT-20260629-P3-UGC-PIPELINE-002

- Executor: claude_code
- Status: complete
- Dispatched: 2026-06-29 19:40:48

---

Done. Wrote `C:\SFV_BLUEPRINT\04_WORKFLOWS\UGC_BUSINESS_PIPELINE.md` after reading all five source files (CLIENT_BANKS.md existed, so it was read and incorporated). I also read `VIDEO_EDIT_WORKFLOW.md` to mirror its consolidated open-decisions table format and labeling conventions, since the directive required matching it.

**What the doc covers** â€” all 10 stages in order, each labeled CANON / UNCONFIRMED / FHR / MISSING:

1. **Lead intake** â€” entry channels, capture schema (mapped to CLIENT_BANKS), CRM candidates (Notion / Airtable / `clients.json` â€” noted `clients.json` is the only one with vault precedent), vault data location.
2. **Brief/proposal** â€” contents, tool candidates, deposit policy (all flagged).
3. **Contract** â€” combined-vs-separate readings, e-sign candidates, key clauses (usage rights / revision limits / late fees) all UNCONFIRMED.
4. **Pre-production** â€” referenced UGC_PRE_PRODUCTION.md without repeating it; defined the **signed-contract â†’ intake-form trigger** as the handoff.
5. **Post-shoot delivery** â€” WeTransfer stop-gap; Pixieset / Frame.io / Drive / portal candidates; platform decision flagged FOR HUMAN REVIEW.
6. **Client notification** â€” channel TBD, flagged MISSING.
7. **Revision loop** â€” intake, tracking via CANON re-versioning names, round limits, overage policy.
8. **Invoicing/payment** â€” timing options, tool candidates (Wave/HoneyBook/Stripe/Square, weighted for recurring billing), invoice contents, late policy.
9. **Client memory update** â€” write-back fields to CLIENT_BANKS, manual-vs-automated trigger.
10. **Performance/reporting** â€” metrics, store, 30-day cadence, flagged MISSING.

**Conventions honored:** frontmatter exactly as specified (STATUS FOR HUMAN REVIEW, v0.1.0, OWNER WILL, CREATED 2026-06-29, CREATED_BY the loop directive ID); no tool decisions invented â€” every open tool choice lists candidates and is explicitly flagged; consolidated 23-row open-decisions table at the end matching VIDEO_EDIT_WORKFLOW.md's format; CONNECTED FILES section linking all six required docs (plus a couple of directly-referenced ones).

One judgment call worth surfacing: I added a Â§0 pipeline diagram and an explicit **sequencing decision** (row 23) because the proposal/contract/deposit ordering is genuinely undecided across the source docs â€” flagged UNCONFIRMED rather than silently picking an order.
