---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-27
CREATED_BY: Claude Chat (Blueprint Builder) — overnight session, Will asleep
PURPOSE: Paper trial run of the SFV_EVENTS Zenfolio QR delivery pipeline, end-to-end, against a realistic
  multi-camera tournament day. Extends 08_TESTS/PAPER_TRIAL_RUNS.md (CANON) — this is "TRIAL 03" in spirit
  but kept as a companion file so the CANON doc is not rewritten by an autonomous session. If approved,
  fold the pointer into PAPER_TRIAL_RUNS.md.
RUNS_AGAINST: 04_WORKFLOWS/EVENTS_ZENFOLIO_DELIVERY.md (FOR HUMAN REVIEW)
---

# PAPER TRIAL — SFV_EVENTS ZENFOLIO QR DELIVERY (multi-camera tournament day)

This walks a realistic tournament day through the locked QR delivery pipeline, step by step, to
find where it breaks before a real 50-subject day does. Method per PAPER_TRIAL_RUNS.md "HOW TO RUN".

---

## SCENARIO (invented, realistic)
- **Event:** one-day grappling tournament. SFV set up as a single Zenfolio event, fresh card stack.
- **Subjects:** 47 athletes want portraits across the day. Walk-up traffic, not pre-booked slots.
- **Cameras:** 3 bodies feeding 3 laptops. Cam1_ (main portrait), Cam2_ (secondary angle),
  Cam3_ (roaming/action-to-portrait).
- **Volume:** ~2,100 frames total by end of day across the 3 streams.
- **The disorder (what real days actually look like):**
  - On subject #23, the photographer shoots the athlete first and remembers the QR card halfway through.
  - Subject #31's QR card is captured but is blurry/underexposed (card half in shadow).
  - Two athletes (#8, #19) share a very similar look and stand in line back-to-back.
  - Cam3 roams and captures 40 action frames of subject #12 BEFORE that subject's QR card is shot at the booth.
  - Around frame 1,500 one laptop's upload stalls (wifi dip at the venue).
  - Subject #44 arrives at the very end; the day's card stack has run out of unused QR cards.

---

## WALKTHROUGH (stage by stage — what happens / what could break)

**1. Event setup (fresh card stack for the day).**
- Happens: SFV creates the Zenfolio event, loads/prepares the QR card stack.
- Break risk: if the card stack is reused from a prior day, QR codes may already map to old galleries.
  → Mitigation EXISTS (doc: "fresh card stack per day, don't carry across days"). OK.
- NEW gap: doc does not state **how many cards are in a stack** or what happens when you run out
  mid-day (see subject #44 below). Capacity planning is undocumented.

**2. Per-subject capture: QR card first, then subject (the Golden Rule).**
- Happens for most subjects: card frame, then portrait frames. Clean delimiter.
- Break (subject #23): athlete shot first, card shot mid-sequence. The frames BEFORE the card now
  belong, by the sort-order logic, to the PREVIOUS subject's run. → Silent misassignment.
  → Mitigation EXISTS as discipline ("Golden Rule + visible check") but there is **no mechanical catch**.
  The system cannot detect that #23's early frames are mis-tagged; it just assigns them to #22.
- Break (subject #12, Cam3 roaming): action frames captured at a different location BEFORE the booth
  QR card. When Cam3's stream is filename-sorted and merged, those 40 frames precede #12's card and
  attach to whoever's card last preceded them in Cam3's sequence. → Cross-subject leak.
  → This is a NEW, important failure mode the doc does NOT cover: **roaming/out-of-order capture on a
  secondary camera breaks the "card-then-subject" assumption that holds at a fixed booth.**

**3. Cull without removing QR frames.**
- Happens: editor culls rejects, keeps QR frames as structural markers.
- Break (subject #31): the QR frame is captured but BLURRY. Two sub-risks:
  (a) the editor culls it on instinct because it "looks like a bad frame" → delimiter lost → EXISTING
      failure mode (culled QR frame). Mitigation EXISTS (exempt QR frames from culling).
  (b) the QR frame is KEPT but the QR code is **unreadable** by Zenfolio because of blur/exposure.
      → NEW failure mode: the doc treats QR frames as binary present/absent, but a present-but-unreadable
      QR is a third state with the same downstream effect (no assignment) and no mitigation listed.

**4. Confirm per-camera prefixes (Cam1_/Cam2_/Cam3_).**
- Happens: prefixes applied per stream.
- Break: if Cam3's card was set up with the wrong prefix (e.g. forgot to set the body's naming), its
  frames collide or sort wrong. → Mitigation EXISTS (prefixes), but depends on per-body config being
  correct BEFORE the day. NEW checklist item: verify each body's filename prefix at setup, not after.

**5. Upload batches sorted by FILENAME (not date).**
- Happens: each stream uploads, filename-sorted, preserving card→subject runs.
- Break (laptop stall ~frame 1,500): a partial upload. If the batch is re-started, are already-uploaded
  frames skipped or duplicated? → NEW open question: the doc does not define upload idempotency /
  resume behavior. A duplicate upload could create a second run of frames and double-assign.
- Break (subtle): if any single stream is accidentally sorted by date (default in some uploaders),
  that stream interleaves → EXISTING failure mode (sort-by-date). Mitigation EXISTS.

**6. Zenfolio QR workflow assigns each run of frames to the preceding QR card's subject.**
- Happens: assignment by delimiter.
- Break (#8 vs #19 similar look, back-to-back): not actually a system break — QR cards make the
  look-alike problem irrelevant (that's the whole reason face-rec was rejected). ✅ The pipeline
  HANDLES this well. Worth noting as a confirmed strength, not a gap.
- Break (compounding): any subject whose delimiter was lost in steps 2–3 (#12, #23, #31) gets frames
  assigned to the wrong gallery or to none. The failure is invisible at this step — it looks successful.

**7. Subject receives/scans their QR-linked gallery, same day.**
- Happens: athlete scans, sees their photos, (upsell) buys/downloads.
- Break (subject #44, card stack exhausted): no card → cannot be entered into the QR workflow at all.
  → NEW failure mode: **running out of QR cards mid-event has no documented fallback.** Does the
  photographer hand-create a gallery? Turn away the sale? This is a revenue-loss path with no plan.
- Break (delivery-time): the affected subjects (#12, #23, #31) either see wrong photos (someone else's
  in their gallery — a privacy problem) or an empty/missing gallery (a service failure) — ON-SITE,
  in front of the customer. This is the worst place to discover the break, which is the whole point
  of running this on paper now.

---

## FAILURE MODES SURFACED

| # | Trigger | User-visible symptom | Mitigation | NEW or EXISTING |
|---|---------|----------------------|------------|-----------------|
| 1 | Subject shot before QR card (Golden Rule violation) | Early frames assigned to previous subject | Discipline + visible check; NO mechanical catch | EXISTING (risk noted) |
| 2 | Roaming 2nd camera captures subject before booth QR card | Action frames leak to wrong gallery | none documented | **NEW** |
| 3 | QR frame present but blurry/unreadable | No assignment despite frame existing | none (doc assumes binary present/absent) | **NEW** |
| 4 | Per-body filename prefix mis-set at setup | Stream collision / wrong sort | Cam1_/2_/3_ prefixes (if set correctly) | EXISTING + new checklist item |
| 5 | Upload stall → restart | Possible duplicate/double-assigned run | none (idempotency undefined) | **NEW** |
| 6 | Stream sorted by date not filename | Interleaved streams break runs | sort-by-filename rule | EXISTING |
| 7 | QR card stack exhausted mid-event | New subject can't be entered; lost sale | none documented | **NEW** |
| 8 | Look-alike subjects back-to-back | (none — handled) | QR cards make look irrelevant | EXISTING STRENGTH ✅ |

---

## GAPS + RECOMMENDATIONS (concrete, for the EVENTS doc)
Add to EVENTS_ZENFOLIO_DELIVERY.md "FAILURE MODES" section:
1. **Roaming/secondary-camera out-of-order capture.** Define a rule: roaming cameras (Cam3) either
   (a) also shoot the subject's QR card at point of capture, or (b) are treated as a separate
   non-QR-assigned stream merged manually. Pick one and document it.
2. **Unreadable QR frame (third state).** Add: QR frames must be legible, not just present. Add a
   capture-time check (chimp the card frame for scannability) and a recovery path (manual gallery
   assignment) when a card is unreadable in post.
3. **Upload idempotency / resume.** Document what happens when an upload is interrupted and restarted —
   does Zenfolio dedupe by filename? If unknown, this is a [FOR HUMAN REVIEW] verification item.
4. **Card-stack capacity + exhaustion fallback.** Document stack size per event and a defined fallback
   when cards run out mid-day (carry a spare stack? manual gallery? cap subjects per stack?).
Add to a pre-event SETUP CHECKLIST (new, small):
5. Verify each camera body's filename prefix (Cam1_/2_/3_) BEFORE first capture.
6. Confirm card stack count vs expected subject volume; carry a spare stack.

## OPEN QUESTIONS FOR WILL
- Q-EV1: How many QR cards in a standard stack, and what is the fallback when they run out mid-event?
- Q-EV2: For roaming Cam3 — does it shoot the subject's QR card at point of capture, or is it a
  manually-merged non-assigned stream? (Determines whether failure mode #2 is real for your setup.)
- Q-EV3: Does Zenfolio's uploader dedupe by filename on a re-started upload, or can it create duplicate
  runs? (Determines whether failure mode #5 is real.)
- Q-EV4: Is there a quick on-site way to detect a mis-assigned gallery before the subject sees it
  (a spot-check step), or is delivery fully trusted to the QR logic?

## VERDICT
The QR pipeline is **robust to the problem it was designed for** (look-alike subjects, no biometrics —
failure mode #8 confirms the design choice was right). It is **fragile to disorder**: out-of-order
capture (#1, #2), degraded-but-present QR frames (#3), upload interruption (#5), and capacity exhaustion
(#7). None of these are exotic — all four are normal occurrences on a busy 47-subject day. The common
thread: **every failure is silent and only surfaces in front of the customer at delivery.** The single
highest-value hardening is a 30-second on-site spot-check (Q-EV4) that turns a silent delivery failure
into a catchable booth-side one. Residual risk after the recommended doc patches: LOW-MEDIUM, dominated
by the unreadable-QR and out-of-order-roaming cases until a mechanical check exists.

## CONNECTED FILES
- [[PAPER_TRIAL_RUNS|Paper Trial Runs]]
- [[EVENTS_ZENFOLIO_DELIVERY|SFV_EVENTS Zenfolio QR Delivery]]
- [[FAILURE_TESTS|Failure Tests]]
- [[EDGE_CASES|Edge Cases]]
