---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
CREATED: 2026-06-29
CREATED_BY: loop directive BLUEPRINT-20260629-P3-UGC-PIPELINE-002
LAST_UPDATED: 2026-06-29
PURPOSE: Blueprint the full UGC money pipeline — everything before and after the shoot that
  converts a prospect into a paying client and closes the loop: lead intake → brief/proposal →
  contract → pre-production handoff → post-shoot delivery → client notification → revision loop →
  invoicing/payment → client-memory update → performance/reporting. Closes MASTER GAP LIST P3
  (BLUEPRINT_COVERAGE_MAP.md §6) and the Domain B business-side holes (steps 1, 2, 15-19).
---

# UGC BUSINESS PIPELINE

> This doc fills the **business-side** holes in the revenue branch. The coverage audit found that
> *"the entire UGC money pipeline before and after the shoot (lead → brief → contract → invoice →
> notify → report) is unblueprinted"* (BLUEPRINT_COVERAGE_MAP.md §2 marks steps **1, 2, 15, 16, 18,
> 19 as MISSING** and steps **15, 17 as THIN**; ranked **P3** in §6 as *"the money branch has no
> blueprint for converting/serving/billing clients."*).
>
> It covers **SFV_UGC** (the primary money engine, Engine Level 6.5). It does **not** re-spec the
> shoot itself — the pre-production app is already CANON in `UGC_PRE_PRODUCTION.md`; this doc only
> defines the handoff into it (§4). The reel edit/QC craft is covered in `VIDEO_EDIT_WORKFLOW.md`
> (FHR) and `QUALITY_CONTROL.md` and is referenced, not repeated.

**STATUS legend (inline labels used throughout this doc)**
- **CANON** — locked, established in another CANON vault doc (cited inline).
- **UNCONFIRMED** — inferred from adjacent docs, or a tool/decision that has not been made.
- **FOR HUMAN REVIEW (FHR)** — Will must ratify before this becomes operational practice.
- **MISSING** — no vault doc or process exists for this step at all.

> **Whole-doc STATUS: FOR HUMAN REVIEW.** Almost the entire business pipeline is first-draft
> inference — there is no prior CANON for lead intake, proposals, contracts, invoicing, notification,
> or reporting. **No tool decision below is locked.** Every open tool choice is flagged with its
> candidate options; do not treat any candidate as adopted until Will ratifies it.

---

## 0. PIPELINE AT A GLANCE

```
PROSPECT
   │
   ▼
[1] LEAD INTAKE ........... capture prospect → CRM record (tool UNCONFIRMED)
   │
   ▼
[2] BRIEF / PROPOSAL ...... deliverables, dates, revisions, price → sent to prospect
   │                         deposit policy UNCONFIRMED
   ▼
[3] CONTRACT ............. usage rights / revision limits / late fees → e-sign (tool UNCONFIRMED)
   │   ── signed contract = the trigger ──────────────┐
   ▼                                                  │
[4] PRE-PRODUCTION ....... triggers pre-pro intake form (UGC_PRE_PRODUCTION.md, CANON)
   │                                                  │
   ▼                                                  │
   ┌──────────── SHOOT + EDIT + QC ─────────────┐     │  (out of scope here:
   │  UGC_PRE_PRODUCTION.md / VIDEO_EDIT_WORKFLOW │     │   see referenced docs)
   │  .md / QUALITY_CONTROL.md                    │     │
   └──────────────────────────────────────────────┘   │
   │                                                  │
   ▼                                                  │
[5] POST-SHOOT DELIVERY ... WeTransfer (stop-gap) → permanent platform FHR
   │
   ▼
[6] CLIENT NOTIFICATION ... "content is ready" — channel MISSING
   │
   ▼
[7] REVISION LOOP ........ requests in → tracked → round limit → overage policy
   │
   ▼
[8] INVOICING / PAYMENT .. deposit + balance? full upfront? — tool UNCONFIRMED
   │
   ▼
[9] CLIENT MEMORY UPDATE . write back to CLIENT_BANKS (perf, style, banned, hooks)
   │
   ▼
[10] PERFORMANCE / REPORT  30-day check-in, results logged — MISSING
   │
   └──────────► feeds back into [1] retention / upsell
```

> **Sequencing note (UNCONFIRMED):** the order of §2 (proposal), §3 (contract) and §8 (invoicing) is
> not yet a decided business process — e.g. whether a deposit invoice (§8) fires at contract-signing
> (§3) or at booking (§2). The diagram shows the *proposed* order; the money-timing decision is
> flagged in §8 and in the open-decisions table. **FHR.**

---

## 1. LEAD INTAKE

**How a prospect enters the system.** Today this is informal — SFV_UGC.md lists named leads
(Brandon Bellotti, Will Wilver / ProEdge) as freeform notes, and CLIENT_BANKS.md holds them as
`STATUS: PROSPECTING` / `WARM_LEAD` profile stubs. There is **no intake form, no CRM, and no defined
entry channel.** *(MISSING — coverage map §2 step 1 = MISSING.)*

### 1.1 Entry channels *(UNCONFIRMED)*
- Inbound DM (Instagram — the growth account, SFV_UGC.md "primary growth account").
- Warm/referral (the current real-world path — both named leads are personal connections).
- Outbound (Will reaching out to niche targets: fitness/athletic trainers first, athletes second).
- **Which channels are in scope and how a lead is logged from each: UNCONFIRMED. FHR.**

### 1.2 Info captured at intake *(proposed schema — UNCONFIRMED)*
Aligns with the eventual CLIENT_BANKS profile (§9) so intake flows straight into client memory:

| Field | Notes | Maps to CLIENT_BANKS |
|---|---|---|
| Name | person or business | `NAME` |
| Niche | fitness trainer / athlete / other | `NICHE` |
| Platform / IG handle | their account(s) | `IG_HANDLE` |
| Goals | growth, sales, rebrand, launch | (new — not in current schema) |
| Budget | self-reported range | informs `PACKAGE` |
| Lead source / channel | DM / referral / outbound | (new) |
| Lead status | PROSPECTING / WARM_LEAD / BOOKED / ACTIVE / PAST | extends current `STATUS` |
| Date entered | YYYYMMDD per NAMING_CONVENTIONS | — |

- **Goals**, **budget**, **lead source**, and a richer **status** are **new fields** not in the
  current CLIENT_BANKS schema (which only has NAME / NICHE / IG_HANDLE / PACKAGE / START_DATE /
  memory fields). Adding them is a proposed CLIENT_BANKS schema extension. **FHR.**

### 1.3 CRM tool — UNCONFIRMED
No CRM is recorded anywhere in the vault. **Candidates (introduced by this directive, none adopted):**
- **Notion** — flexible, doc-native; pairs well with a vault-style mental model; weak as a true CRM.
- **Airtable** — relational, good for a client/lead pipeline with views and automations.
- **`clients.json`** — the lightest option, and the **only one with any vault precedent**:
  CLIENT_BANKS.md / coverage map §2 step 5 reference client memory living in `clients.json`. A simple
  JSON store keeps lead + client memory in one engine-readable file (favours automation, §9).

> **⚑ FOR HUMAN REVIEW — pick the CRM / lead store.** The `clients.json` option is the only one with
> existing vault grounding and the cleanest path to the automated client-memory write-back in §9; a
> hosted CRM (Notion/Airtable) is friendlier for manual pipeline management but adds a second source
> of truth. **Do not adopt any until ratified.**

### 1.4 Where the record lives in the vault *(UNCONFIRMED)*
- **Architecture (this doc + CLIENT_BANKS.md)** lives in the vault under `12_DATABANKS/`.
- **Data** (the actual lead/client records) follows the two-layer model noted in the coverage map
  (§3: *"vault = architecture, SFV_ENGINE/DATABANKS/ = data"*) — i.e. records live in the engine data
  store, not in the vault prose. Exact path **UNCONFIRMED** — confirm against DATABANK_ARCHITECTURE.md
  / CLIENT_BANKS.md. **FHR.**

---

## 2. BRIEF / PROPOSAL

**What gets sent before the client books.** Currently **MISSING** — no proposal template, tool, or
deposit policy exists in the vault (coverage map §2 step 2 = MISSING).

### 2.1 Proposed proposal contents *(UNCONFIRMED)*
- **Deliverables** — e.g. "X reels / month" per the chosen package. Package definitions are
  themselves **UNCONFIRMED** (SFV_UGC.md PACKAGES = UNCONFIRMED: *"Base: X reels per month;
  add-ons: hard posts, generated ads, lifestyle shoots; varies by client type"*).
- **Service tier** — Standard (engine-led, scalable batch) vs Premium (Will-led, virality-focused,
  higher price). *(CANON-described in SFV_UGC.md SERVICE TIERS; pricing UNCONFIRMED.)*
- **Shoot date(s)** — proposed capture date(s).
- **Revision rounds** — number of included revision rounds (ties to §7). Count **UNCONFIRMED**.
- **Turnaround / SLA** — draft-delivery time after shoot, and per-revision turnaround. **UNCONFIRMED.**
- **Price + deposit terms** — see §2.3 and §8.
- **Usage / scope summary** — pointer to the contract clauses (§3).

### 2.2 Proposal / contract tool — UNCONFIRMED
No tool recorded. **Candidates (none adopted):** HoneyBook, Dubsado, Bonsai (all-in-one proposal +
contract + invoice client-flow tools), or a plain PDF/Google Doc proposal paired with a separate
e-sign + invoice tool. Note the strong overlap with §3 (contract) and §8 (invoicing): an all-in-one
tool (e.g. HoneyBook) could collapse proposal + contract + deposit + invoice into one flow — that is
a **single combined tool decision**, flagged jointly in §8 and the open-decisions table. **FHR.**

### 2.3 Deposit policy — UNCONFIRMED
Whether a deposit is required to book, and how much (e.g. 50% to reserve the shoot date, balance on
delivery), is **undecided and undocumented.** Interacts with §8 invoicing timing. **FHR.**

---

## 3. CONTRACT

**Whether the brief doubles as the contract or is a separate document — UNCONFIRMED.** No contract,
template, or e-sign tool exists in the vault (coverage map §2 step 2 = MISSING). Two readings, both
**FHR:**
- **Reading A — combined:** an all-in-one tool (§2.2) where the proposal *is* the bookable, signable
  agreement (deliverables + terms + deposit in one accepted document).
- **Reading B — separate:** a short proposal to sell, then a standalone contract to sign before any
  pre-production begins.

### 3.1 E-sign tool — UNCONFIRMED
No tool recorded. **Candidates (none adopted):** DocuSign, Dropbox Sign (HelloSign), PandaDoc, or the
built-in e-sign inside an all-in-one tool (HoneyBook/Dubsado/Bonsai, §2.2). **FHR.**

### 3.2 Key clauses *(ALL UNCONFIRMED — drafts for Will to ratify, not legal advice)*
- **Usage rights** — what the client may do with delivered content (organic vs paid ads, duration,
  exclusivity, whitelisting), and **SFV's right to repost** to the SFV_UGC showcase grid
  (SFV_UGC.md: *"Main grid: polished client content showcase, advertising"* — implies SFV reuses
  client work as portfolio/advertising, so a portfolio-use clause is needed). **UNCONFIRMED.**
- **Revision limits** — contractual cap on included revision rounds (mirrors §2.1 / §7); defines what
  triggers paid overage. **UNCONFIRMED.**
- **Late fees** — penalty for late client payment (ties to §8 late-payment policy). **UNCONFIRMED.**
- Other clauses likely needed but **MISSING/UNCONFIRMED:** kill/cancellation fee, reschedule policy,
  deposit non-refundability, content-approval/sign-off, music-licensing responsibility (note the
  open music-licensing decision in VIDEO_EDIT_WORKFLOW.md §3), confidentiality, payment schedule.

> **⚑ FOR HUMAN REVIEW — all contract terms.** Every clause above is a first-draft placeholder.
> Usage rights especially must be settled before paid delivery (it governs what both parties may do
> with the reels). Consider professional/legal review. **Nothing here is a locked term.**

---

## 4. PRE-PRODUCTION *(handoff only — see UGC_PRE_PRODUCTION.md, CANON)*

Pre-production is **already fully covered** by `UGC_PRE_PRODUCTION.md` (CANON; coverage map §1 and §2
step 3 = COVERED — the React intake app spec). **This doc does not repeat it.**

**Handoff point defined here:**
- **The signed contract (§3) is the trigger that opens the pre-production intake form.** A prospect
  does not enter pre-pro until the agreement is signed (and, per the §2.3/§8 deposit decision,
  possibly until the deposit invoice is paid). *(UNCONFIRMED as a written rule — this handoff is
  proposed here; the gating condition (signature only vs signature + deposit) is **FHR**.)*
- At handoff, the lead record (§1) flips status PROSPECTING/WARM_LEAD → **BOOKED**, and the captured
  intake fields (§1.2) plus client memory (§9) feed the pre-pro app — the wiring of CLIENT_BANKS /
  CONTENT_BANKS into the intake form is itself **THIN/UNCONFIRMED** (coverage map §2 steps 4-5,
  P10). See `UGC_PRE_PRODUCTION.md` for the form itself.

---

## 5. POST-SHOOT DELIVERY

**How the finished reel reaches the client** after edit (VIDEO_EDIT_WORKFLOW.md) and QC
(QUALITY_CONTROL.md; SFV_UGC.md: AI self-audit → Will reviews before delivery).

### 5.1 Current method — WeTransfer *(stop-gap, CANON-as-current-state)*
- DELIVERY.md (UNCONFIRMED) records UGC delivery platform as *"[UNCONFIRMED — direct download, Drive
  link, or portal?]"* and CURRENT DELIVERY METHOD = **WeTransfer**, *"used currently, will be replaced
  by proper delivery system."* Coverage map §2 step 15 marks this THIN/MISSING.
- WeTransfer is explicitly a **stop-gap**, not the intended permanent system.

### 5.2 Permanent platform candidates *(none adopted)*
| Candidate | Fit notes | Status |
|---|---|---|
| **Pixieset** | Already in the stack for SFV_STUDIO photo galleries (CANON). Photo/gallery-oriented; video delivery is secondary. Reusing it keeps tooling consistent. | candidate |
| **Frame.io** | Built for video review + versioned approvals + timestamped comments → naturally serves the revision loop (§7). Heavier/pricier. | candidate |
| **Google Drive link** | Cheapest, simplest; no review UX, no branding, weak versioning. | candidate |
| **Client portal** | A branded portal (possibly the R&D Terminal "client review gateway", Role 2, coverage map §3) — most professional, most build effort, and Role 2's inbound network path is itself UNDEFINED/blocked. | candidate / future |

### 5.3 File naming at delivery *(CANON — NAMING_CONVENTIONS.md)*
Client-facing deliverable is renamed at hand-off:
`[CLIENT_ID]_[YYYYMMDD]_[DELIVERABLE]_v[##]` → e.g. `PROEDGE_20250601_REEL_v01`.
Working/review reels use `[BRANCH]_[YYYYMMDD]_[CLIENT]_REEL_[###]_[STATUS]` (DRAFT/APPROVED/REJECTED).
*(CANON; see VIDEO_EDIT_WORKFLOW.md §8.1.)*

> **⚑ FOR HUMAN REVIEW — permanent delivery platform.** This is the platform decision the coverage
> map (P6) and DELIVERY.md leave open. Frame.io aligns best with the revision loop (§7); Pixieset
> reuses existing tooling; a portal is the long-game. **The platform choice is FOR HUMAN REVIEW —
> do not adopt any candidate until Will ratifies it.**

---

## 6. CLIENT NOTIFICATION

**How the client is told their content is ready.** **MISSING** — coverage map §2 step 16 = MISSING;
DELIVERY.md leaves SFV_STUDIO notification *"[UNCONFIRMED — auto or manual?]"* and says nothing for
UGC. There is **no defined channel, template, or trigger.**

### 6.1 Channel — TBD *(MISSING)*
- **Candidates:** email, SMS, Instagram DM (the same channel many leads arrive on, §1.1).
- **Manual vs automated:** could be a manual Will message, or auto-fired by the delivery platform
  (most §5.2 candidates can email a "gallery ready" link automatically) or by the engine/n8n.
- **What it carries:** the delivery link (§5), a short note, revision-round reminder (§7), and — per
  §8 timing — the balance invoice or payment link.

> **⚑ FOR HUMAN REVIEW / MISSING — define the notification step.** Pick a channel, decide
> manual-vs-automated, and write a template. Until then the "content ready" handoff has no defined
> mechanism. **FHR.**

---

## 7. REVISION LOOP

How revision requests come in, how they're tracked, the round limit, and overage handling. The
*naming* of revision states is CANON; the *business process* is UNCONFIRMED.

### 7.1 How requests come in *(UNCONFIRMED)*
- Channel depends on the §5 delivery platform: Frame.io gives timestamped in-video comments;
  Pixieset/Drive/WeTransfer would rely on the §6 notification channel (email/DM) for freeform
  requests. **UNCONFIRMED — tied to the §5 platform decision.**

### 7.2 How tracked *(CANON naming, UNCONFIRMED process)*
- Re-versioning uses NAMING_CONVENTIONS / VIDEO_EDIT_WORKFLOW.md §2.1:
  `..._REEL_[###]_DRAFT` → on feedback `..._REEL_[###]_REJECTED` → new cut →
  `..._REEL_[###]_APPROVED`; client-facing version bumps `_v01 → _v02`. *(CANON.)*
- Approved/rejected outcomes **train the engine over time** (CANON — SFV_UGC.md QUALITY CONTROL).
- **Where the round count is tracked (CRM record §1 / clients.json / delivery platform): UNCONFIRMED.**

### 7.3 Round limits & overage *(UNCONFIRMED)*
- Included revision rounds are set in the proposal (§2.1) and capped in the contract (§3.2). The
  **number is UNCONFIRMED** (SFV_UGC.md PACKAGES UNCONFIRMED; VIDEO_EDIT_WORKFLOW.md §2.1 lists
  "revision-round count / SLA per tier" as FHR).
- **If the client exceeds included rounds:** proposed handling = paid overage (per-revision fee) or
  upsell to a higher tier, billed via §8. **Policy UNCONFIRMED. FHR.**

---

## 8. INVOICING / PAYMENT

**MISSING** — no invoicing tool, schedule, or late-payment policy exists (coverage map §2 step 19 =
MISSING).

### 8.1 When the invoice is sent *(UNCONFIRMED — pick one)*
- **Deposit + balance:** deposit to book (§2.3) → balance on/before delivery (§5/§6).
- **Full upfront:** entire fee before the shoot.
- **Net-terms:** full invoice on delivery, due in N days.
- **Recommended-to-decide-together:** this is the §2.3 deposit decision and the §0 sequencing note —
  resolve as one money-timing policy. **UNCONFIRMED. FHR.**

### 8.2 Invoicing tool — UNCONFIRMED
No tool recorded. **Candidates (none adopted):** **Wave** (free invoicing/accounting), **HoneyBook**
(all-in-one — would also cover §2 proposal + §3 contract), **Stripe** (payment links / cards / subs —
good fit for a recurring retainer), **Square**. Because SFV_UGC is a **recurring retainer**
(SFV_UGC.md PURPOSE: *"recurring content retainer service"*), a tool that handles **recurring/
subscription billing** (Stripe, or HoneyBook recurring) is worth weighting. **FHR.**

### 8.3 Invoice contents *(proposed — UNCONFIRMED)*
Client name/business, CLIENT_ID, package/tier + deliverables, billing period (retainer month), line
items (base + any add-ons: hard posts, generated ads, lifestyle shoots per SFV_UGC.md), any revision
overage (§7.3), deposit credited, balance due, due date, payment methods, late-fee terms (§3.2).

### 8.4 Late-payment policy — UNCONFIRMED
Late fee / grace period / pause-of-service on non-payment — undecided; ties to the §3.2 late-fee
clause. **FHR.**

> **⚑ FOR HUMAN REVIEW — combined money-tooling decision.** §2.2 (proposal), §3.1 (e-sign), and §8.2
> (invoicing) can be one all-in-one tool (HoneyBook/Dubsado/Bonsai) or a best-of-breed stack
> (e.g. PDF proposal + Dropbox Sign + Stripe). **Decide proposal/contract/invoicing tooling together**
> to avoid three disconnected systems. Recurring-retainer billing should weight the choice. **FHR.**

---

## 9. CLIENT MEMORY UPDATE

After delivery, what gets written back to **CLIENT_BANKS** (UNCONFIRMED). The schema already exists
(CLIENT_BANKS.md) but is **THIN/UNCONFIRMED** and not wired to anything (coverage map §2 step 17 =
THIN).

### 9.1 Fields written back *(per CLIENT_BANKS.md schema — CANON structure, UNCONFIRMED process)*
| Field | What gets written after a delivery |
|---|---|
| `PERFORMANCE_LOG` | reel results over time (feeds from §10 — views/saves/follows/feedback) |
| `HOOK_MEMORY` | which hooks performed for this client (winning hooks → CONTENT_BANKS HOOK_BANK) |
| `PACING_MEMORY` | what edit pace works for them |
| `BANNED_STYLES` | what didn't work / client rejected → avoid next batch |
| `STATUS` | ACTIVE / retained / churned (extends §1.2 status) |

- This closes the loop into pre-production: client memory feeds the next shoot's intake (§4,
  UGC_PRE_PRODUCTION.md) and the hook/script pull (CONTENT_BANKS.md). Wiring is **THIN** today.

### 9.2 Who triggers it *(UNCONFIRMED)*
- **Manual by Will** — Will writes notes back after each batch (matches current reality; no
  automation exists).
- **Automated by the engine** — on Will's accept/reject decision, the engine (n8n / Python) writes
  the outcome to `clients.json` and logs training data (overlaps the THIN training-data automation,
  coverage map P18). This is the cleaner long-game and favours the `clients.json` CRM option (§1.3).
- **Decision UNCONFIRMED — manual now, automate later is the likely path. FHR.**

---

## 10. PERFORMANCE / REPORTING

How results are tracked after the client posts. **MISSING** — coverage map §2 step 18 = MISSING:
*"none (PERFORMANCE_LOG is a field name only)."* The CLIENT_BANKS `PERFORMANCE_LOG` field exists but
there is **no collection method, no store, and no cadence.**

### 10.1 Metrics *(proposed — UNCONFIRMED)*
- Per-reel: **views, saves, shares, follows gained**, watch-through, plus **client feedback** (their
  subjective read). Source = client-reported and/or Instagram Insights (manual export — no IG
  analytics integration is documented).

### 10.2 Where logged *(UNCONFIRMED)*
- Into `PERFORMANCE_LOG` in the client's CLIENT_BANKS record (§9) — i.e. the CRM/`clients.json` store
  (§1.3). No separate reporting store is defined. **UNCONFIRMED.**

### 10.3 Cadence *(proposed — UNCONFIRMED)*
- **30-day check-in** per delivered batch/retainer month: pull results, log to PERFORMANCE_LOG,
  update client memory (§9), and use as the retention/upsell touchpoint (feeds back to §1). Cadence
  is **proposed, not set.** A monthly check-in could be a `send_later`/n8n reminder. **FHR.**

> **⚑ FOR HUMAN REVIEW / MISSING — define reporting.** Pick the metric set, the collection method
> (manual IG Insights vs client-reported vs future integration), the store, and the cadence. Nothing
> exists today. **FHR.**

---

## OPEN DECISIONS — CONSOLIDATED (FOR HUMAN REVIEW)

| # | Decision | § | Status |
|---|---|---|---|
| 1 | Lead entry channels in scope + how each is logged | 1.1 | UNCONFIRMED |
| 2 | Add goals / budget / lead-source / richer-status fields to CLIENT_BANKS schema | 1.2 | UNCONFIRMED |
| 3 | **CRM / lead store: Notion vs Airtable vs `clients.json`** | 1.3 | **FHR** |
| 4 | Vault/data location of lead+client records (DATABANK two-layer path) | 1.4 | UNCONFIRMED |
| 5 | Package definitions + per-tier pricing (gates proposal contents) | 2.1 | UNCONFIRMED |
| 6 | Turnaround / SLA (draft + per-revision) | 2.1 | UNCONFIRMED |
| 7 | Deposit policy (required? how much? when?) | 2.3 | FHR |
| 8 | **Proposal/contract tool (all-in-one vs separate)** | 2.2 | **FHR** |
| 9 | Brief doubles as contract, or separate doc? | 3 | FHR |
| 10 | **E-sign tool: DocuSign / Dropbox Sign / PandaDoc / all-in-one** | 3.1 | **FHR** |
| 11 | Contract clauses — usage rights, revision limits, late fees (+ cancellation, music) | 3.2 | FHR |
| 12 | Pre-pro handoff gate: signature only vs signature + deposit paid | 4 | FHR |
| 13 | **Permanent delivery platform: Pixieset / Frame.io / Drive / portal** (replace WeTransfer) | 5.2 | **FHR** |
| 14 | **Client notification channel (email/SMS/DM) + manual vs auto + template** | 6 | FHR / MISSING |
| 15 | How revision requests come in (tied to platform) | 7.1 | UNCONFIRMED |
| 16 | Where revision-round count is tracked | 7.2 | UNCONFIRMED |
| 17 | Included revision-round count + overage policy (paid / upsell) | 7.3 | UNCONFIRMED |
| 18 | Invoice timing: deposit+balance vs full upfront vs net-terms | 8.1 | UNCONFIRMED |
| 19 | **Invoicing tool: Wave / HoneyBook / Stripe / Square** (weight recurring billing) | 8.2 | **FHR** |
| 20 | Late-payment policy (fee / grace / service pause) | 8.4 | UNCONFIRMED |
| 21 | Client-memory write-back trigger: manual (Will) vs automated (engine) | 9.2 | UNCONFIRMED |
| 22 | Reporting: metric set, collection method, store, 30-day cadence | 10 | FHR / MISSING |
| 23 | Overall pipeline sequencing (proposal/contract/deposit order) | 0 | UNCONFIRMED |

**Cross-doc dependencies that gate this pipeline becoming operational:**
SFV_UGC.md PACKAGES + pricing ratified · CLIENT_BANKS.md promoted from UNCONFIRMED + schema extended ·
DELIVERY.md UGC platform decision · UGC_PRE_PRODUCTION.md intake-form wiring to CLIENT_BANKS/
CONTENT_BANKS (P10) · training-data automation (P18) for the §9 automated write-back · combined
money-tooling decision (CRM #3 + proposal/contract #8/#10 + invoicing #19).

---

## CONNECTED FILES
- [[SFV_UGC|SFV_UGC — Branch Definition]]
- [[DELIVERY|Delivery Workflow]]
- [[UGC_PRE_PRODUCTION|UGC Pre-Production]]
- [[CLIENT_BANKS|Client Banks]]
- [[NAMING_CONVENTIONS|Naming Conventions]]
- [[VIDEO_EDIT_WORKFLOW|Video Edit Workflow]]
- [[QUALITY_CONTROL|Quality Control]]
- [[CONTENT_BANKS|Content Banks]]
- [[BLUEPRINT_COVERAGE_MAP|Blueprint Coverage Map]]
