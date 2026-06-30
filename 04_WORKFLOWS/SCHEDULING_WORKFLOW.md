---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
CREATED: 2026-06-30
CREATED_BY: finishing-loop directive BLUEPRINT-LOOP-20260630-184129-P4-IG-SCHEDULING-001
LAST_UPDATED: 2026-06-30
PURPOSE: Blueprint the Instagram scheduling workflow for the 8 non-MYTHOLOGY branches —
  closes MASTER GAP LIST item P4 (Instagram scheduling, MISSING). Doc-only; no live service touched.
---

# INSTAGRAM SCHEDULING WORKFLOW

Blueprint for how finished, approved posts move from DELIVERY into a scheduling tool and out
to Instagram for the 8 non-MYTHOLOGY branches. This is the home for the gap the
[[BLUEPRINT_COVERAGE_MAP]] flags as: *"Instagram scheduling | all 8 non-MYTHOLOGY branches |
Engine Body | UNCONFIRMED (Later? Buffer?) | none | **MISSING**."*

**Status of this doc:** FOR HUMAN REVIEW — nothing here is CANON. The scheduling tool is undecided
(see §7) and **no timing value (post frequency, time-of-day, time zone) exists anywhere in the vault**,
so every cadence number below is flagged UNCONFIRMED. This doc proposes the *structure*; Will ratifies
the values and the tool.

---

## 1. SCOPE

**In scope — 8 branches that get engine scheduling** (source: [[DELIVERY]] → INSTAGRAM DELIVERY,
STATUS: UNCONFIRMED):

| Branch | Engine Level (per DELIVERY.md) | Caption tag (per NAMING_CONVENTIONS, CANON) |
|---|---|---|
| SFV_EVENTS | Level 5–6.5 | `[SFV EVENTS|##]` |
| SFV_STUDIO | Level 5.5 | `[SFV STUDIO|##]` |
| SFV_UGC | Level 6.5 | `[SFV UGC|##]` |
| SFV_LIVE | Level 3.5 | `[SFV LIVE|##]` |
| SFV_ATHLETICS | Level 3.5 | `[SFV ATHLETICS|##]` |
| SFV_ARCHIVE | Level 3.5 | `[SFV ARCHIVE|##]` |
| SFV_WORLD | Level 2.5 | `[SFV WORLD|##]` |
| SFV_404 | Level 2.5 | `[SFV 404|##]` |

**Out of scope:**
- **MYTHOLOGY / `abbass` account** — Level 1, **manual / direct posting** (source: [[DELIVERY]], [[INTEGRATIONS]]).
  Not routed through any scheduling tool. Do not blueprint a scheduling path for it here.
- The "Level" values above are the **only** vault-recorded posting signal. What a Level *means* in
  concrete terms (posts per day/week, priority weighting) is **[UNCONFIRMED]** — it is not defined in
  [[DELIVERY]], [[INTEGRATIONS]], or any file reviewed for this doc. Do not infer a posts-per-week number
  from a Level until Will defines the Level scale.

---

## 2. PER-BRANCH POSTING CADENCE & TIMING RULES

> **[UNCONFIRMED — entire section.]** The vault records a relative *intensity* per branch (the Level)
> but **no cadence (how often), no time-of-day, and no time zone.** The table below is a *template to be
> filled by Will*, not a recommendation. Cells marked `[UNCONFIRMED]` must not be guessed.

| Branch | Relative intensity (vault: Level) | Posts / week | Preferred post window | Notes |
|---|---|---|---|---|
| SFV_UGC | Highest (6.5) | [UNCONFIRMED] | [UNCONFIRMED] | Client/revenue branch; cadence may be client-driven, not fixed |
| SFV_EVENTS | High (5–6.5) | [UNCONFIRMED] | [UNCONFIRMED] | Event-driven bursts; may post same-day on-site (see DELIVERY turnaround) |
| SFV_STUDIO | High (5.5) | [UNCONFIRMED] | [UNCONFIRMED] | Same-day turnaround on shoot days |
| SFV_LIVE | Medium (3.5) | [UNCONFIRMED] | [UNCONFIRMED] | — |
| SFV_ATHLETICS | Medium (3.5) | [UNCONFIRMED] | [UNCONFIRMED] | — |
| SFV_ARCHIVE | Medium (3.5) | [UNCONFIRMED] | [UNCONFIRMED] | Evergreen; least time-sensitive |
| SFV_WORLD | Low (2.5) | [UNCONFIRMED] | [UNCONFIRMED] | — |
| SFV_404 | Low (2.5) | [UNCONFIRMED] | [UNCONFIRMED] | — |

**Timing rules to be DECIDED by Will (each is FOR HUMAN REVIEW):**
- **Time zone** for all schedule slots — [UNCONFIRMED].
- Whether cadence is a **fixed weekly grid** per branch, or an **on-demand** "queue when approved" model,
  or a hybrid. [UNCONFIRMED].
- **Event/shoot-day overrides** (EVENTS, STUDIO) where same-day delivery may bypass the normal grid —
  noted in [[DELIVERY]] (same-day turnaround) but no scheduling rule exists. [UNCONFIRMED].
- Whether the engine **Level** should drive a queue-priority or auto-cadence value once defined. [FOR HUMAN REVIEW].

---

## 3. CAPTION INSERTION

**Source of truth: [[NAMING_CONVENTIONS]] → CAPTION SYSTEM (Instagram). STATUS: CANON.**

Every scheduled post carries the branch caption tag, which is **CANON** and must be applied exactly:

```
[SFV LIVE|01]      [SFV ATHLETICS|01]
[SFV EVENTS|01]    [SFV UGC|01]
[SFV STUDIO|01]    [SFV WORLD|01]
[SFV ARCHIVE|01]   [SFV 404|01]
```

**CANON rules (verbatim from NAMING_CONVENTIONS):**
- The number is **sequential per branch**.
- It is **consistent across all posts**.
- **Never skip numbers.**

**Workflow implications (these are blueprint structure, not new CANON):**
- The caption tag is the **first line** of the caption block. [INFERENCE — NAMING_CONVENTIONS lists the
  tags but does not state position; confirm placement with Will.]
- The **sequence counter is per-branch and global to the branch** (not per-project, not per-tool). Whatever
  schedules the post must read and increment the last-used number for that branch so no number is skipped or
  reused. Where that counter lives (a vault file, a JSON state file under `%SFV_ROOT%`, or the scheduling
  tool's own post history) is **[UNCONFIRMED]** — see open-decisions table.
- For a **carousel**, the tag is applied **once to the single caption** of the carousel post (a carousel is
  one IG post with one caption), not once per slide. See §4.
- The remaining caption body (copy, CTAs, hashtags) is **[UNCONFIRMED / out of scope here]** — no caption-copy
  system is recorded in the reviewed vault files beyond the tag. Do not invent one.

---

## 4. CAROUSEL vs STANDALONE HANDLING

> Instagram treats a carousel as **one post with one caption and 2–10 ordered media items**; a standalone
> is one post with one media item. The scheduling structure differs only in asset grouping and ordering.

**Standalone post:**
- One exported asset (photo or reel) → one scheduled post → one caption block (with one branch tag).
- Asset naming follows [[NAMING_CONVENTIONS]] (`[BRANCH]_[YYYYMMDD]_[EVENT/CLIENT]_[SPEC]_[####]` for photo
  exports; `[BRANCH]_[YYYYMMDD]_[CLIENT]_REEL_[###]_[STATUS]` for reels).

**Carousel post:**
- 2–10 exported assets grouped into one post, in a **defined slide order**.
- **Ordering mechanism is [UNCONFIRMED].** NAMING_CONVENTIONS' 4-digit sequence (`_0001`, `_0002`, …) is the
  natural ordering key [INFERENCE], but the vault does not state that carousel slide order = file sequence.
  Confirm with Will whether slide order is driven by the filename sequence or set manually in the tool.
- **One caption, one branch tag** for the whole carousel (§3).
- **Mixed media in one carousel** (photos + reel/video) — whether allowed and how it's specced is
  **[UNCONFIRMED]**; no vault rule exists.

**[FOR HUMAN REVIEW]** — A small naming/grouping convention for "these N files = one carousel, in this order"
does not exist in the vault. Options: a shared sub-sequence, a folder convention, or a manifest field in the
hand-off (§5). Will to decide; do not invent the convention here.

---

## 5. HAND-OFF FROM DELIVERY

This workflow begins where [[DELIVERY]] ends. DELIVERY (STATUS: UNCONFIRMED) routes finished content two ways:
client delivery (STUDIO/EVENTS/UGC) **and** "content goes directly to Instagram" for the other branches.
Scheduling consumes the **Instagram-bound** stream.

**Hand-off chain (blueprint):**

```
EXPORT  →  (QC / Will approval)  →  DELIVERY (Instagram-bound)  →  SCHEDULING (this doc)  →  Instagram
```

**Pre-conditions a post must satisfy before it enters scheduling (proposed gate — [FOR HUMAN REVIEW]):**
1. Asset is **approved** (reels carry `_APPROVED` status per NAMING_CONVENTIONS; the QC/approval gate is
   defined in [[QUALITY_CONTROL]], referenced by DELIVERY). [INFERENCE that `_APPROVED` is the scheduling gate
   for reels — confirm.]
2. Asset is **export-spec correct** (photo SPEC / reel encode). Export specs are themselves **[UNCONFIRMED]**
   in [[EXPORT]] ("specs TBD") — flagged upstream, not resolved here.
3. Asset is **named per [[NAMING_CONVENTIONS]]** (CANON).
4. The post's **branch, type (standalone/carousel), and caption tag number** are known.

**What hands the asset over is [UNCONFIRMED]:** DELIVERY currently lists WeTransfer as the *client* delivery
stop-gap, but says nothing about how an Instagram-bound, approved asset is staged for the scheduler (a watched
folder under `%SFV_ROOT%`? a manual upload into the tool? an n8n step — see §6?). This staging mechanism is a
**MISSING** link and a required decision.

---

## 6. n8n INTEGRATION POINT (DOC-ONLY)

> **Do not touch, start, stop, or reconfigure the live n8n instance.** This section describes a *possible*
> integration point in text only. No workflow is to be built or imported as part of this doc.

**Context from the vault:**
- [[INTEGRATIONS]] (UNCONFIRMED) lists **N8N [FUTURE]**: *"workflow orchestration and model routing … connects
  Engine scripts, local models, Claude API, scheduling tools."* — i.e. the scheduling tool is named as an
  intended n8n connection, but no workflow exists.
- [[BLUEPRINT_COVERAGE_MAP]] notes n8n is in reality **LIVE (v2.22.5)** while TOOL_STATUS still says FUTURE
  (a known stale-doc contradiction). The integration below stays **doc-only** regardless of live status.

**Proposed integration point (blueprint only, [FOR HUMAN REVIEW]):**
- A future n8n workflow could watch the staging location (§5), read the asset + its branch/type/caption-tag,
  increment the per-branch caption counter (§3), and push the post to the scheduling tool **via that tool's
  API** (if the chosen tool exposes one — see §7).
- **API availability depends on the tool decision** and is **[UNCONFIRMED]** for both candidates. If the chosen
  tool has no usable scheduling API, this stays **manual** (export → human uploads into the tool's calendar).
- The n8n route is **optional and downstream of the tool decision** — it must not be built until (a) the tool
  is chosen, (b) its API is confirmed, and (c) Will approves wiring it. Until then, scheduling is **manual
  upload into the chosen tool**.

---

## 7. SCHEDULING TOOL DECISION — FOR HUMAN REVIEW

**Status: UNDECIDED. The blueprint does not pick.** [[DELIVERY]] and [[INTEGRATIONS]] both record the choice as
**UNCONFIRMED (Later vs Buffer)**. The hard requirement that *is* recorded: the tool **must handle 8+ Instagram
accounts** (DELIVERY) / the 8 engine-scheduled accounts (INTEGRATIONS).

**Decision criteria to evaluate against (Will to fill the verdicts):**

| Criterion | Why it matters here | Later | Buffer |
|---|---|---|---|
| Native multi-account (≥8 IG accounts) | Hard requirement (DELIVERY) | [VERIFY] | [VERIFY] |
| Per-account / per-branch scheduling queues | 8 branches, different cadences (§2) | [VERIFY] | [VERIFY] |
| **Carousel** scheduling support | §4 requires it | [VERIFY] | [VERIFY] |
| **Reel / video** scheduling support | UGC/LIVE/etc. post reels | [VERIFY] | [VERIFY] |
| Visual calendar / per-branch time grid | Needed for §2 cadence model | [VERIFY] | [VERIFY] |
| Public scheduling **API** (for §6 n8n) | Determines manual vs automated | [VERIFY] | [VERIFY] |
| Plan that covers 8 accounts + **price** | Cost gate | [UNCONFIRMED — do not guess price] | [UNCONFIRMED — do not guess price] |

> **All cells above are intentionally left as `[VERIFY]` / `[UNCONFIRMED]`.** Per the no-invention rule, this
> doc does **not** assert feature support or pricing for either product. Will (or a separate, sourced tool-research
> pass) fills these from each vendor's current docs before deciding. The comparison is a *checklist*, not a claim.

**This decision belongs in [[FOR_HUMAN_REVIEW/PROPOSALS]] and, once ratified, in [[DECISIONS]].** It is a
prerequisite for §6 (n8n) and for finalizing §2–§5.

---

## 8. CONSOLIDATED OPEN DECISIONS / UNCONFIRMED TABLE

| # | Item | Current state | Label | Owner / next step |
|---|---|---|---|---|
| 1 | Scheduling tool (Later vs Buffer vs other) | Undecided; 8+ accounts is the only fixed requirement | FOR HUMAN REVIEW | Will → PROPOSALS → DECISIONS |
| 2 | Meaning of the engine "Level" scale (Level → posts/week) | Levels exist in DELIVERY; meaning undefined | UNCONFIRMED | Will defines the scale |
| 3 | Per-branch cadence (posts/week) | No value in vault | UNCONFIRMED | Will fills §2 table |
| 4 | Per-branch time-of-day / post window | No value in vault | UNCONFIRMED | Will fills §2 table |
| 5 | Time zone for all schedules | Not recorded | UNCONFIRMED | Will |
| 6 | Cadence model: fixed grid vs on-demand vs hybrid | Not recorded | FOR HUMAN REVIEW | Will |
| 7 | Event/shoot-day same-day override rule | Same-day turnaround noted; no scheduling rule | UNCONFIRMED | Will |
| 8 | Caption tag position in caption block | CANON tag exists; position not stated | INFERENCE → confirm | Will |
| 9 | Where the per-branch caption sequence counter lives | Not recorded | UNCONFIRMED | Will / future build |
| 10 | Carousel slide-ordering mechanism | Sequence key inferred, not stated | UNCONFIRMED | Will |
| 11 | Carousel grouping/naming convention ("N files = 1 carousel") | Does not exist | FOR HUMAN REVIEW | Will |
| 12 | Mixed photo+video carousels allowed? | No rule | UNCONFIRMED | Will |
| 13 | Staging mechanism: DELIVERY → scheduler hand-off | Missing link | MISSING | Will / design pass |
| 14 | Scheduling gate = reel `_APPROVED` status? | Inferred from naming + QC | INFERENCE → confirm | Will |
| 15 | Export specs for IG (photo SPEC / reel encode) | "specs TBD" in EXPORT | UNCONFIRMED (upstream) | EXPORT.md owner |
| 16 | n8n auto-push vs manual upload | Depends on tool API | FOR HUMAN REVIEW (after #1) | Will (doc-only until approved) |
| 17 | Tool API availability (both candidates) | Unknown | UNCONFIRMED | Tool-research pass |
| 18 | Plan/pricing for 8-account coverage | Unknown; do not guess | UNCONFIRMED | Tool-research pass |

---

## CONNECTED FILES
- [[BLUEPRINT_COVERAGE_MAP|Blueprint Coverage Map]]
- [[DELIVERY|Delivery Workflow]]
- [[NAMING_CONVENTIONS|Naming Conventions]]
- [[INTEGRATIONS|Integrations]]
- [[EXPORT|Export]]
- [[QUALITY_CONTROL|Quality Control]]
- [[N8N_BLUEPRINT|n8n Blueprint]]
- [[FOR_HUMAN_REVIEW/PROPOSALS|Proposals for Human Review]]
- [[DECISIONS|Decisions]]
