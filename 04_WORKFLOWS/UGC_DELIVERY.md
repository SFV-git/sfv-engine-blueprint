---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
CREATED: 2026-06-30
CREATED_BY: finishing-loop directive BLUEPRINT-LOOP-20260630-184410-P6-UGC-DELIVERY-001
LAST_UPDATED: 2026-06-30
PURPOSE: Blueprint the UGC client-delivery sub-system end-to-end — how a finished, QC-passed reel
  reaches a paying client and how the client is told it is ready. Deep-dives the delivery platform
  decision (currently WeTransfer stop-gap) and the missing notification step, and wires both into
  UGC_BUSINESS_PIPELINE.md steps 15-17 (delivery / notification / client-memory update). Pricing and
  tool choices are NOT decided here — they are flagged FOR HUMAN REVIEW.
---

# UGC CLIENT DELIVERY

> **Scope.** This doc is the **delivery half** of the UGC money pipeline: it takes over at the moment
> a reel has been edited and QC-passed, and ends when the client has the files, has been notified, and
> the result is logged back to client memory. It is a **focused expansion** of
> `UGC_BUSINESS_PIPELINE.md` §5 (post-shoot delivery), §6 (client notification), and §9 (client-memory
> update) — i.e. **coverage-map steps 15, 16, 17**. It does **not** re-spec the shoot, the edit, or
> QC (see `UGC_PRE_PRODUCTION.md` CANON, `VIDEO_EDIT_WORKFLOW.md` FHR, `QUALITY_CONTROL.md`), and it
> does **not** cover invoicing (`UGC_BUSINESS_PIPELINE.md` §8).
>
> Branch: **SFV_UGC** — the primary money engine (Engine Level 6.5, `SFV_UGC.md`).

**STATUS legend (inline labels used throughout)**
- **CANON** — locked in another CANON vault doc (cited inline).
- **CANON-in-practice** — a real, current behaviour the vault had not previously written down (noted as such).
- **UNCONFIRMED** — inferred from adjacent docs, or a decision not yet made.
- **FOR HUMAN REVIEW (FHR)** — Will must ratify before this becomes operational practice.
- **MISSING** — no vault doc or process exists for this at all.

> **Whole-doc STATUS: FOR HUMAN REVIEW.** The delivery platform and the notification step are both
> unresolved in the vault today (`DELIVERY.md` UGC platform = *"[UNCONFIRMED — direct download, Drive
> link, or portal?]"*; notification = undefined). **No tool decision below is locked.** Nothing here
> may be promoted to CANON without Will's ratification.

---

## 0. WHERE THIS SITS IN THE PIPELINE

```
                 ┌─────────── UGC_BUSINESS_PIPELINE.md (the full money loop) ───────────┐
   ... shoot ──► [5] DELIVERY ──► [6] NOTIFICATION ──► [7] REVISION ──► [8] INVOICE ──► [9] MEMORY ...
                     │                  │                   │                               │
                     └──────────────────┴───────────────────┴───────────────────────────────┘
                                 THIS DOC expands steps 15 / 16 / 17 ↑
```

Coverage-map → pipeline mapping (from `UGC_BUSINESS_PIPELINE.md` and `BLUEPRINT_COVERAGE_MAP.md` §2):

| Coverage-map step | Pipeline § | What it is | Prior status | This doc |
|---|---|---|---|---|
| **15** | §5 | Post-shoot delivery (file → client) | THIN / MISSING (WeTransfer stop-gap) | §2–§3 |
| **16** | §6 | Client notification ("content is ready") | **MISSING** | §4 |
| **17** | §9 | Client-memory write-back after delivery | THIN | §6 |

> The revision loop (pipeline §7) and invoicing (pipeline §8) sit *between* notification and
> memory-update. They are **referenced** here where delivery touches them, but they are **owned by**
> `UGC_BUSINESS_PIPELINE.md` and are not re-decided in this doc.

---

## 1. CURRENT STATE — WeTransfer stop-gap

- `DELIVERY.md` (STATUS: UNCONFIRMED) records:
  - **CURRENT DELIVERY METHOD = WeTransfer** — *"used currently, will be replaced by proper delivery
    system."* → **CANON-in-practice** as the *current* behaviour (it is what happens today); the vault
    already names it, but it is explicitly a **stop-gap**, not the intended system.
  - **SFV_UGC platform = "[UNCONFIRMED — direct download, Drive link, or portal?]"** → the permanent
    platform is **undecided**.
- `SFV_UGC.md` defines an **OUTPUT PATH** of `%BRANCHES_ROOT%\SFV_UGC\EXPORT\` and
  `%BRANCHES_ROOT%\SFV_UGC\DELIVERY\` (**CANON** branch paths) — i.e. there is already a local
  `DELIVERY\` staging folder; what is missing is the **outbound platform** the client actually pulls
  from, and the **notification** that tells them to.

**Gaps this doc addresses:** (a) the permanent delivery platform is **FHR**; (b) the notification step
is **MISSING**; (c) the write-back to client memory is **THIN/UNCONFIRMED**.

---

## 2. DELIVERY PATH — END TO END *(proposed — UNCONFIRMED process, CANON where cited)*

The reel has been edited (`VIDEO_EDIT_WORKFLOW.md`) and has passed QC + Will's review
(`SFV_UGC.md` QUALITY CONTROL: *"AI self-audits each reel batch before delivery … Will reviews before
posting"* — **CANON**). From there:

```
[A] APPROVED MASTER        Will-approved cut exists  (gate: do not deliver un-approved work)
        │                  master named  ..._REEL_[###]_APPROVED   (CANON, NAMING_CONVENTIONS)
        ▼
[B] STAGE LOCALLY          copy/export into %BRANCHES_ROOT%\SFV_UGC\DELIVERY\   (CANON path, SFV_UGC.md)
        │
        ▼
[C] RENAME CLIENT-FACING   [CLIENT_ID]_[YYYYMMDD]_[DELIVERABLE]_v[##]
        │                  e.g. PROEDGE_20250601_REEL_v01            (CANON, see §2.1)
        ▼
[D] UPLOAD / PUBLISH       push to the chosen delivery PLATFORM      (platform = FHR, §3)
        │
        ▼
[E] NOTIFY CLIENT          "your content is ready" + link            (channel = MISSING, §4)
        │
        ▼
[F] REVISION WINDOW        client reviews → requests come back       (owned by pipeline §7)
        │                  re-version  _v01 → _v02 ; DRAFT→REJECTED→APPROVED  (CANON naming)
        ▼
[G] FINAL ACCEPT           client signs off on final version
        │
        ▼
[H] MEMORY WRITE-BACK      log outcome to CLIENT_BANKS               (THIN today, §6)
```

- **Gate at [A]:** nothing is delivered until Will has approved — this is already CANON behaviour in
  `SFV_UGC.md`; written here as the explicit entry gate. **CANON-in-practice** as an entry condition.
- **[B]/[C] paths and naming are CANON.** The platform at **[D]** and the channel at **[E]** are the
  two open decisions (§3, §4).

### 2.1 File naming at delivery *(CANON — NAMING_CONVENTIONS.md)*
- **Client-facing deliverable:** `[CLIENT_ID]_[YYYYMMDD]_[DELIVERABLE]_v[##]`
  → e.g. `PROEDGE_20250601_REEL_v01`.
- **Working / review reels:** `[BRANCH]_[YYYYMMDD]_[CLIENT]_REEL_[###]_[STATUS]`, where STATUS ∈
  {DRAFT, REJECTED, APPROVED} (`VIDEO_EDIT_WORKFLOW.md` §8.1). Client-facing revisions bump the
  version suffix `_v01 → _v02`. *(CANON.)*

### 2.2 What is delivered *(proposed — UNCONFIRMED)*
- The approved reel(s) for the batch/retainer month. Whether delivery also includes raw/source files,
  multiple aspect-ratio cuts (e.g. 9:16 + 1:1), captions/subtitle files, or a thumbnail is
  **UNCONFIRMED** — it depends on package definitions, which are themselves UNCONFIRMED
  (`SFV_UGC.md` PACKAGES). **FHR.**

---

## 3. DELIVERY PLATFORM — FOR HUMAN REVIEW

> **⚑ FOR HUMAN REVIEW — pick the permanent delivery platform (replaces WeTransfer).** This is the
> decision `DELIVERY.md` and the coverage map (P6) leave open. The directive scopes the choice to
> **client portal vs Google Drive vs Pixieset**; `UGC_BUSINESS_PIPELINE.md` §5.2 additionally lists
> **Frame.io** as a fourth candidate — carried below for completeness. **Do not adopt any candidate
> until Will ratifies it.**

### 3.1 The three primary candidates — trade-offs for a *revenue* branch

This is a **paying-client, recurring-retainer** branch (`SFV_UGC.md` PURPOSE: *"recurring content
retainer service. Primary money engine."*). The platform is part of the product experience, so weight
**professionalism / brand**, **review-and-revision UX** (the revision loop is pipeline §7), and
**recurring-month repeatability**, not just raw file transfer.

| | **Client portal** (branded) | **Google Drive link** | **Pixieset** |
|---|---|---|---|
| **What it is** | A branded review/delivery gateway — possibly the R&D Terminal "client review gateway" (Role 2, `BLUEPRINT_COVERAGE_MAP.md` §3) | Shared folder / share link | Gallery delivery platform already in the stack for **SFV_STUDIO** photo galleries (CANON, `DELIVERY.md`) |
| **Professionalism / brand** | **Highest** — fully SFV-branded, premium feel that matches the "primary money engine" positioning | Low — generic Google UI, no branding, reads as informal | Medium-high — clean branded galleries; built for client delivery |
| **Built for video?** | Designed for whatever SFV builds | Holds any file, but no video-review UX | **Photo/gallery-oriented**; video delivery is secondary (per `UGC_BUSINESS_PIPELINE.md` §5.2) |
| **Revision-loop fit (§7)** | Can be built around versioned review/sign-off | None — feedback happens off-platform (via §4 channel) | Limited; relies on the §4 notification channel for freeform revision requests |
| **Tooling consistency** | New system to build/run | Ubiquitous, zero new tooling | **Reuses an existing CANON tool** — one fewer platform in the stack |
| **Build / setup effort** | **Highest** — and Role 2's inbound network path is itself UNDEFINED/blocked (coverage map §3) | **Lowest** — works today | Low — account/config only; already operated for SFV_STUDIO |
| **Cost** | UNCONFIRMED (do not invent) | Free / existing storage | UNCONFIRMED (do not invent) |
| **Best when** | SFV wants a premium, owned client experience as the long game | A fast, free upgrade over WeTransfer is "good enough" for now | Will wants brand + minimal new tooling by reusing the studio platform |

### 3.2 Fourth candidate carried from the pipeline doc *(not in the directive's three, listed for completeness)*
- **Frame.io** — purpose-built for **video review + versioned approvals + timestamped comments**, so
  it serves the revision loop (§7) most naturally; heavier/pricier. *(From `UGC_BUSINESS_PIPELINE.md`
  §5.2. Cost UNCONFIRMED — do not invent.)*

### 3.3 Decision framing *(no recommendation made — Will decides)*
- **Google Drive** = the cheapest, fastest replacement for the WeTransfer stop-gap, at the cost of
  brand and any review UX.
- **Pixieset** = keeps the toolset consistent with SFV_STUDIO and adds branding, at the cost of being
  photo-first (video is secondary).
- **Client portal** = the most professional, most "owned" experience and the long-game, at the cost of
  the most build effort (and a currently-blocked inbound path).
- The choice also **shapes the revision loop (§7)**: a portal or Frame.io can carry structured,
  versioned feedback in-platform; Drive/Pixieset push revision requests onto the §4 notification
  channel (email/DM) as freeform messages. **This platform decision and the §7 revision-intake
  decision should be made together. FHR.**

---

## 4. CLIENT NOTIFICATION — MISSING

**How the client is told their content is ready.** **MISSING** — `BLUEPRINT_COVERAGE_MAP.md` §2 step
16 = MISSING; `DELIVERY.md` leaves even SFV_STUDIO notification as *"[UNCONFIRMED — auto or manual?]"*
and says nothing for UGC. There is **no defined channel, template, or trigger today.**

### 4.1 Channel — TBD *(MISSING)*
- **Candidates:** email, SMS, or **Instagram DM** (the same channel many leads arrive on —
  `UGC_BUSINESS_PIPELINE.md` §1.1; SFV_UGC is the primary growth/DM account). **UNCONFIRMED.**

### 4.2 Manual vs automated *(UNCONFIRMED)*
- **Manual** — Will sends the "ready" message himself (matches current reality; no automation exists).
- **Automated by the platform** — most §3 candidates can auto-email a "gallery/files ready" link on
  upload (Pixieset, a portal, Frame.io). Google Drive would rely on a manual or engine-sent message.
- **Automated by the engine** — n8n/Python fires the notification on the [D]→[E] handoff (§2). This is
  the long-game and pairs with the automated memory write-back (§6). **UNCONFIRMED. FHR.**

### 4.3 What the notification carries *(proposed — UNCONFIRMED)*
- The **delivery link** (§3 platform), a short branded note, the **revision-round reminder** (how many
  rounds are included and how to request them — pipeline §7), and — **per the pipeline §8 money-timing
  decision** — the **balance invoice / payment link** if balance-on-delivery is the chosen model.
  *(Invoice inclusion depends on `UGC_BUSINESS_PIPELINE.md` §8.1, which is UNCONFIRMED.)*

### 4.4 Template *(MISSING — to be drafted)*
- No notification template exists in the vault. A short, branded, channel-appropriate template should
  be drafted once the channel (§4.1) is chosen. **MISSING.**

> **⚑ FOR HUMAN REVIEW / MISSING — define the notification step.** Pick a channel (§4.1), decide
> manual-vs-automated (§4.2), confirm what it carries (§4.3, incl. whether the invoice rides along),
> and write the template (§4.4). Until then the "content ready" handoff has **no defined mechanism.**

---

## 5. CONNECTION TO REVISION LOOP *(pointer — owned by UGC_BUSINESS_PIPELINE.md §7)*

Delivery feeds directly into the revision loop, so the two touch here:
- **Where revision requests come in depends on the §3 platform** — a portal/Frame.io can capture
  in-platform versioned/timestamped feedback; Pixieset/Drive route freeform requests through the §4
  notification channel. *(`UGC_BUSINESS_PIPELINE.md` §7.1 — UNCONFIRMED, tied to the platform choice.)*
- **Re-versioning naming is CANON:** `..._REEL_[###]_DRAFT` → on feedback `_REJECTED` → new cut →
  `_APPROVED`; client-facing `_v01 → _v02` (§2.1).
- **Round count + overage policy are UNCONFIRMED** and owned by pipeline §7.3 / `SFV_UGC.md` PACKAGES —
  **not decided here, and no number is invented.**

---

## 6. CLIENT-MEMORY WRITE-BACK *(coverage-map step 17 — THIN; owned by UGC_BUSINESS_PIPELINE.md §9)*

After final accept ([G]→[H], §2), the delivery outcome is written back to **CLIENT_BANKS** so the next
batch is smarter. The schema exists (`CLIENT_BANKS.md`) but is **THIN/UNCONFIRMED** and not yet wired
to anything (coverage map §2 step 17 = THIN).

- **Fields touched at delivery** (per `CLIENT_BANKS.md` schema — CANON structure, UNCONFIRMED process):
  `PERFORMANCE_LOG`, `HOOK_MEMORY`, `PACING_MEMORY`, `BANNED_STYLES`, `STATUS`
  (full detail in `UGC_BUSINESS_PIPELINE.md` §9.1 — not duplicated here).
- **Trigger — UNCONFIRMED:** manual by Will now (matches reality) vs automated by the engine later
  (write to `clients.json` on Will's accept/reject) — `UGC_BUSINESS_PIPELINE.md` §9.2. **FHR.**
- **Why it lives in this doc:** the write-back is the **closing event of the delivery path** ([H]). The
  *what/why/how* is owned by pipeline §9; this doc only marks it as the terminal step of delivery and
  flags that the trigger and the CRM/`clients.json` store are unresolved. **THIN/UNCONFIRMED.**

---

## 7. WHAT IS CANON vs OPEN HERE *(quick read)*

- **CANON (already locked, cited):** local `EXPORT\` + `DELIVERY\` branch paths (`SFV_UGC.md`);
  client-facing + working file naming (`NAMING_CONVENTIONS.md` / `VIDEO_EDIT_WORKFLOW.md` §8.1);
  "Will reviews before delivery" QC gate (`SFV_UGC.md`); re-version naming for revisions.
- **CANON-in-practice (current behaviour, now written down):** WeTransfer is the *current* delivery
  method (stop-gap); "do not deliver un-approved work" as the entry gate at [A].
- **FOR HUMAN REVIEW:** the permanent delivery platform (§3); the notification channel + manual/auto +
  template (§4).
- **MISSING:** the notification mechanism as a whole (no channel/template/trigger exists today).
- **UNCONFIRMED:** exactly what files are delivered (§2.2); revision-request intake (§5, tied to
  platform); memory write-back trigger (§6).

---

## OPEN DECISIONS — CONSOLIDATED (FOR HUMAN REVIEW)

| # | Decision | § | Status | Notes / dependency |
|---|---|---|---|---|
| D1 | **Permanent delivery platform: client portal vs Google Drive vs Pixieset** (+ Frame.io carried from pipeline) — replaces WeTransfer | 3 | **FHR** | = `UGC_BUSINESS_PIPELINE.md` open-decision #13; coverage-map step 15 / P6 |
| D2 | What is delivered (reel only? + raws / multi-ratio / captions / thumbnail?) | 2.2 | UNCONFIRMED | gated by `SFV_UGC.md` PACKAGES (UNCONFIRMED) |
| D3 | **Notification channel: email / SMS / Instagram DM** | 4.1 | **FHR / MISSING** | = pipeline open-decision #14; coverage-map step 16 |
| D4 | Notification manual vs platform-auto vs engine-auto | 4.2 | UNCONFIRMED | engine-auto pairs with D7 |
| D5 | What the notification carries (incl. whether balance invoice rides along) | 4.3 | UNCONFIRMED | depends on pipeline §8.1 money-timing |
| D6 | Notification template (draft once channel chosen) | 4.4 | MISSING | blocked on D3 |
| D7 | Revision-request intake channel (in-platform vs §4 channel) | 5 | UNCONFIRMED | **decide jointly with D1**; owned by pipeline §7.1 |
| D8 | Client-memory write-back trigger: manual (Will) vs automated (engine → `clients.json`) | 6 | UNCONFIRMED | = pipeline open-decision #21; coverage-map step 17 |

**Cross-doc dependencies that gate UGC delivery becoming operational:**
`DELIVERY.md` UGC platform decision (D1) · `SFV_UGC.md` PACKAGES ratified (gates D2) ·
`UGC_BUSINESS_PIPELINE.md` §7 revision policy (D7) and §8 money-timing (D5) ·
`CLIENT_BANKS.md` promoted from UNCONFIRMED + wired for the §6 write-back (D8) ·
R&D Terminal Role 2 "client review gateway" inbound path is UNDEFINED/blocked (affects the portal
option in D1, `BLUEPRINT_COVERAGE_MAP.md` §3).

> **Reminder:** no pricing, settings, or tool decisions are made in this doc. Every candidate above is
> a candidate only. Nothing here is CANON until Will ratifies it.

---

## CONNECTED FILES
- [[UGC_BUSINESS_PIPELINE|UGC Business Pipeline]] — parent doc; this expands its §5 / §6 / §9 (steps 15-17)
- [[DELIVERY|Delivery Workflow]] — current-state source (WeTransfer stop-gap; UGC platform UNCONFIRMED)
- [[SFV_UGC|SFV_UGC — Branch Definition]] — branch paths, QC gate, packages (UNCONFIRMED)
- [[UGC_PRE_PRODUCTION|UGC Pre-Production]] — upstream (shoot intake; CANON)
- [[VIDEO_EDIT_WORKFLOW|Video Edit Workflow]] — upstream edit + file-status naming
- [[QUALITY_CONTROL|Quality Control]] — pre-delivery QC gate
- [[CLIENT_BANKS|Client Banks]] — client-memory store for the §6 write-back
- [[NAMING_CONVENTIONS|Naming Conventions]] — client-facing + working file naming (CANON)
- [[BLUEPRINT_COVERAGE_MAP|Blueprint Coverage Map]] — step 15 / 16 / 17 source of record
