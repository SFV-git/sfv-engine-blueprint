---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-25
CREATED_BY: Claude Chat (Blueprint Builder) - formalization pass, Will away
SOURCE: Decisions locked in conversation + memory; no vault doc previously existed (flagged top-priority in MISSING_REFERENCED_FILES.md section 3)
---

# SFV_EVENTS - ZENFOLIO QR DELIVERY WORKFLOW

This is the locked on-site, same-day delivery system for SFV_EVENTS (on-site portrait
sessions at events/tournaments). It existed only in chat history + memory until this doc.
Content below is the locked operational system; items needing external verification are
tagged [FOR HUMAN REVIEW]. Promote to CANON once the verification block is cleared.

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

## OPEN VERIFICATION ITEMS (clear these to promote -> CANON)
1. Zenfolio Sports & Events Advanced plan: current caps, pricing, feature set. [FHR]
2. QR card stock / source - where cards are produced/printed, format. [FHR - referenced as missing in MISSING_REFERENCED_FILES.md]
3. QR export / card-generation format from Zenfolio. [FHR]
4. Per-day event template - reusable Zenfolio event setup per tournament day. [FHR - referenced as missing]
5. 3-laptops / 1-account concurrency under Advanced plan terms. [FHR]
6. Cross-link confirmed: DELIVERY.md SFV_EVENTS line now points here (was UNCONFIRMED).

## CONNECTED FILES
- [[DELIVERY|Delivery Workflow]]
- [[EXPORT|Export]]
- [[CULLING|Culling]]
- [[SFV_EVENTS|SFV Events]]
- [[INGEST|Ingest Workflow]]
