---
STATUS: FOR HUMAN REVIEW
VERSION: v0.2.0
OWNER: WILL
LAST_UPDATED: 2026-06-30
CREATED_BY: Claude Chat (Blueprint Builder) - formalization pass, Will away
UPDATED_BY: finishing-loop directive BLUEPRINT-LOOP-20260630-184711-P7-ZENFOLIO-CANON-001 - open-item resolution pass (CANON-ready, not promoted)
SOURCE: Decisions locked in conversation + memory; no vault doc previously existed (flagged top-priority in MISSING_REFERENCED_FILES.md section 3)
---

# SFV_EVENTS - ZENFOLIO QR DELIVERY WORKFLOW

This is the locked on-site, same-day delivery system for SFV_EVENTS (on-site portrait
sessions at events/tournaments). It existed only in chat history + memory until this doc.
Content below is the locked operational system; items needing external verification are
tagged [FOR HUMAN REVIEW]. Promote to CANON once the verification block is cleared.

---

## READY-TO-PROMOTE NOTE (for Will)
**The operational core of this workflow is CANON-ready.** The locked recipe — QR-card-before-subject
(Golden Rule), per-day fresh card stacks, Cam1_/Cam2_/Cam3_ filename prefixes, filename-sorted upload,
same-day on-site delivery, face-rec rejected — is battle-tested and complete. None of the 5 open items
below change that recipe; they are **external/undecided facts** (Zenfolio plan terms, card sourcing,
export format, a not-yet-built template) that the vault has never recorded.

This pass **resolved all 5 to an honest disposition** rather than inventing values — see the
RESOLUTION OF OPEN ITEMS section. Each is now labelled UNCONFIRMED (external verification, Will must
check Zenfolio) or MISSING (build artifact, not yet created). **None blocks the correctness of the
workflow logic**; items 1 and 5 block only capacity/cost planning, item 4 is a build task.

**Recommendation:** Will may promote the operational doc to CANON now while keeping the open items as a
standing [FOR HUMAN REVIEW] verification block (they are external facts, not internal contradictions).
Per the project canon-control rule this doc is left at **STATUS: FOR HUMAN REVIEW** — it is NOT
self-promoted. Flip to CANON only on Will's explicit say-so.

---

## PURPOSE
Deliver event/tournament portraits to subjects on the same day, on-site, with each subject
able to find only their own photos - using a QR card per subject rather than face
recognition. Instant delivery is itself the upsell.

## LOCKED STACK
- Platform: Zenfolio Sports & Events, Advanced plan. [FOR HUMAN REVIEW - confirm current Advanced-plan caps/pricing/feature set at purchase time]
- Delivery mechanism: QR Code Workflow - each subject is associated with a QR card; the card links the subject to their gallery/photos.
- Model: same-day, on-site. Subject scans/receives their QR-linked gallery the day of.
- Face recognition: REJECTED. QR cards are the deliberate alternative.

## THE GOLDEN RULE (non-negotiable)
Photograph the QR card BEFORE shooting the subject.
The QR frame is the delimiter that assigns every following frame to that subject. If the QR
card is not captured, or is culled/missed, that subject's photos cannot be auto-assigned and
delivery breaks for them. The QR frame must survive culling - see Failure Modes.

## MULTI-DAY EVENT STRUCTURE
A multi-day tournament is run as separate Zenfolio events - one per day - each with a fresh
card stack. Do not carry a card stack across days; each day stands alone.
[INFERENCE - the rule is one event + fresh stack PER DAY; "three events" maps to a typical
3-day tournament, not a hard count. Confirm wording.]

## CAMERA / FILENAME CONVENTION
- Per-camera filename prefixes: Cam1_, Cam2_, Cam3_. These prevent filename collision when multiple camera streams feed one event.
- Upload batches are sorted by FILENAME, not date taken. This keeps the QR-card-then-subject ordering intact across merged streams. Sorting by capture time would interleave streams and break the QR-to-subject association.

## ON-SITE HARDWARE
- 3 laptops, 1 Zenfolio account. [FOR HUMAN REVIEW - confirm Advanced plan permits 3 concurrent uploader sessions on one account; plan-terms question.]
- Maps to the 3 camera streams (Cam1/2/3).

## WORKFLOW - STEP BY STEP
1. Set up the event in Zenfolio for the day (fresh card stack).
2. For each subject: shoot the QR card first, then shoot the subject.
3. Cull WITHOUT removing QR frames (the QR frame is structural, not a keeper photo).
4. Confirm per-camera prefixes (Cam1_/Cam2_/Cam3_).
5. Upload batches sorted by filename.
6. Zenfolio QR workflow assigns each run of frames to the subject whose QR card precedes them.
7. Subject receives/scans their QR-linked gallery - same day, on-site.

## FAILURE MODES (known, locked)
- Culled QR frame -> subject's photos lose their delimiter -> auto-assignment fails for that subject. Mitigation: QR frames exempt from culling; treat as structural markers.
- Missed QR frame (Golden Rule violation - subject shot before card) -> no delimiter -> same break. Mitigation: discipline + a visible on-camera/laptop check.
- Filename collision across cameras -> wrong frames assigned. Mitigation: Cam1_/2_/3_ prefixes. Never upload mixed streams without prefixes.
- Sort-by-date instead of filename -> streams interleave -> QR-to-subject runs break. Mitigation: always sort upload batches by filename.

## UPSELL MODEL
Instant / same-day delivery is the product differentiator and the upsell - subjects get their
portraits on-site rather than waiting. [FOR HUMAN REVIEW - confirm pricing/packaging if specced.]

## REJECTED ALTERNATIVES
- Face recognition: rejected in favor of QR cards (reliability/control + no biometric dependency on-site).

## RESOLUTION OF OPEN ITEMS (P7-ZENFOLIO-CANON pass, 2026-06-30)
Each of the 5 items was checked against the whole vault. **No vault doc records a value for any of
them** — confirmed by grep across the blueprint and by MISSING_REFERENCED_FILES.md §1/§3, which itself
flags these as undocumented. Per the no-assumptions rule they are resolved to UNCONFIRMED/MISSING, NOT
to invented values. Disposition below.

**Item 1 — Zenfolio Sports & Events Advanced plan: caps / pricing / feature set.**
- Status: **UNCONFIRMED (external verification).** Nowhere in the vault. This is a vendor fact that also
  drifts over time, so it cannot be "locked" in blueprint text the way an internal rule can.
- To clear: Will reads Zenfolio's current Advanced (Sports & Events) plan page at purchase/renewal time
  and records storage cap, gallery/event limits, and price into this doc.
- Blocks: capacity & cost planning only. Does NOT block the workflow logic.

**Item 2 — QR card stock / source (where cards are produced/printed, and physical format).**
- Status: **UNCONFIRMED / MISSING.** No vault doc says whether cards are Zenfolio-generated, printed
  in-house, or ordered from a third party; no stock/size/material recorded. Referenced as missing in
  MISSING_REFERENCED_FILES.md §1 and §3.
- To clear: Will specifies (a) card SOURCE — Zenfolio-exported vs self-printed vs vendor — and (b) card
  STOCK — physical size, material, finish, and where reprinted. Feeds the per-day stack-capacity
  question raised in PAPER_TRIAL_SFV_EVENTS.md (Q-EV1: cards per stack + exhaustion fallback).
- Blocks: on-site supply/logistics. Does NOT block the workflow logic.

**Item 3 — QR export / card-generation format from Zenfolio.**
- Status: **UNCONFIRMED (external verification).** Whether Zenfolio's QR Code Workflow exports cards as
  a PDF sheet, individual images, or print-shop file — and at what spec — is not recorded anywhere in
  the vault and depends on Zenfolio's current feature set.
- To clear: Will confirms the actual export artifact Zenfolio's QR workflow produces and records the
  format here. Directly tied to Item 2 (source) and to the unreadable-QR failure mode surfaced in the
  paper trial (a present-but-unscannable card has the same downstream effect as a missing one).
- Blocks: card production pipeline detail. Does NOT block the workflow logic.

**Item 4 — Per-day event template (reusable Zenfolio event setup per tournament day).**
- Status: **MISSING (build artifact, not yet created).** The doc describes the per-day structure (one
  Zenfolio event per day, fresh card stack) but no reusable TEMPLATE object/checklist exists. Referenced
  as missing in MISSING_REFERENCED_FILES.md §1.
- To clear: build a per-day event template — either a Zenfolio saved-event template or a setup checklist
  in this vault — capturing event-name pattern, card-stack assignment, and the 3-laptop/Cam-prefix
  config. PAPER_TRIAL_SFV_EVENTS.md §GAPS items 5–6 (verify each body's prefix at setup; confirm stack
  count vs expected volume) are the natural seed for this checklist.
- Blocks: setup repeatability/speed. Does NOT block the workflow logic.

**Item 5 — 3 laptops / 1 Zenfolio account concurrency under Advanced plan terms.**
- Status: **UNCONFIRMED (external verification / plan terms).** Whether Advanced permits 3 concurrent
  uploader sessions on one account is a Zenfolio ToS/plan question not recorded in the vault. The
  3-laptop → Cam1/2/3 mapping is locked operationally; the account-terms permission for it is not
  verified.
- To clear: Will confirms against Zenfolio account/plan terms that 3 simultaneous uploader sessions on
  one login are allowed (or identifies the per-seat requirement). If not allowed, the on-site hardware
  model needs revisiting.
- Blocks: on-site concurrency assumption. Does NOT block the single-stream workflow logic.

**Item 6 — Cross-link (DELIVERY.md → this doc).**
- Status: **RESOLVED.** DELIVERY.md §SFV_EVENTS now reads "Zenfolio Sports & Events (Advanced) — QR Code
  Workflow. See [[EVENTS_ZENFOLIO_DELIVERY]]" — the old "UNCONFIRMED" is gone. Verified this pass.
- **BUT see the SFV_EVENTS.md contradiction flag below — a second doc was missed.**

---

## [FOR HUMAN REVIEW] CONTRADICTION FLAG — SFV_EVENTS.md still says delivery is UNCONFIRMED
**Flagged, not silently fixed** (SFV_EVENTS.md is STATUS: CANON; per the file-editing + human-approval
rules a CANON branch doc is not edited without Will's say-so).

- **Where:** `02_BRANCHES/SFV_EVENTS.md`, the `## DELIVERY [UNCONFIRMED]` section (≈ lines 35-37).
- **Current text:**
  > `## DELIVERY [UNCONFIRMED]`
  > `- Same day to client`
  > `- Delivery method: Pixieset (like Studio) or different? UNCONFIRMED`
- **Contradiction:** Zenfolio is the **locked** delivery decision (this doc; DELIVERY.md; UNCONFIRMED.md
  resolved line; memory). The branch doc still offers "Pixieset or different? UNCONFIRMED," which is
  stale and contradicts canon. Pixieset is the **SFV_STUDIO** platform, not Events.
- **Proposed one-line correction (for Will to ratify):** replace the DELIVERY block with —
  > `## DELIVERY`
  > `- Same day, on-site to subject`
  > `- Delivery method: Zenfolio Sports & Events (Advanced) — QR Code Workflow. See [[EVENTS_ZENFOLIO_DELIVERY]]`
  and drop the `[UNCONFIRMED]` tag on the heading.
- **Action required:** Will approves → a follow-up session edits SFV_EVENTS.md (CANON) and logs it. This
  doc does NOT make that edit.

---

## CONSOLIDATED OPEN DECISIONS / UNCONFIRMED TABLE
| # | Item | Disposition | Blocks workflow logic? | To clear |
|---|------|-------------|------------------------|----------|
| 1 | Zenfolio Advanced plan caps / pricing / feature set | UNCONFIRMED (external, time-varying) | No — capacity/cost planning only | Will reads current Zenfolio Advanced plan page; record caps + price |
| 2 | QR card stock / source (produce/print/format) | UNCONFIRMED / MISSING | No — supply/logistics | Will specifies card source + physical stock; record here |
| 3 | QR export / card-generation format from Zenfolio | UNCONFIRMED (external) | No — production detail | Will confirms Zenfolio QR-workflow export artifact + spec |
| 4 | Per-day event template (reusable setup) | MISSING (build artifact) | No — setup repeatability | Build template/checklist (seed: paper-trial gaps 5-6) |
| 5 | 3 laptops / 1 account concurrency under Advanced terms | UNCONFIRMED (external / plan terms) | No — concurrency assumption | Will confirms Zenfolio allows 3 concurrent uploader sessions on one login |
| 6 | Cross-link DELIVERY.md → this doc | RESOLVED | — | Done (verified 2026-06-30) |
| 7 | SFV_EVENTS.md DELIVERY still says "Pixieset or different? UNCONFIRMED" | FOR HUMAN REVIEW (contradicts canon) | No — but stale canon | Will ratifies the proposed one-line correction; follow-up session edits CANON doc |
| 8 | Paper-trial hardening (roaming Cam3, unreadable QR, upload idempotency, stack exhaustion) | UNCONFIRMED — open questions Q-EV1..Q-EV4 | Hardening, not core logic | See PAPER_TRIAL_SFV_EVENTS.md §GAPS + §OPEN QUESTIONS |

> Note: Items 1, 3, 5 are **external vendor facts** — they cannot be "locked" in blueprint text and are
> expected to stay as a standing verification block even after the operational doc is promoted to CANON.
> Items 2, 4 are **internal decisions/build tasks** Will still owes. Item 7 is a **canon contradiction**
> in another doc. None contradicts the locked recipe in this doc.

## CONNECTED FILES
- [[DELIVERY|Delivery Workflow]]
- [[EXPORT|Export]]
- [[CULLING|Culling]]
- [[SFV_EVENTS|SFV Events]]
- [[INGEST|Ingest Workflow]]
- [[PAPER_TRIAL_SFV_EVENTS|Paper Trial — SFV_EVENTS Zenfolio QR Delivery]]
- [[PAPER_TRIAL_RUNS|Paper Trial Runs]]
- [[MISSING_REFERENCED_FILES|Missing / Referenced-But-Absent]]
- [[UNCONFIRMED|Unconfirmed Items]]
