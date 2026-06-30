---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
CREATED: 2026-06-30
CREATED_BY: finishing-loop directive BLUEPRINT-LOOP-20260630-183735-P1-CONTENT-IDEA-BANK-001
LAST_UPDATED: 2026-06-30
PURPOSE: Blueprint R&D Terminal Role 5 — the Content Idea Bank — the connective engine that turns
  24/7 research (RESEARCH_BANKS) into shoot-ready, reusable content elements (CONTENT_BANKS). Closes
  the §3 / Role 5 MISSING gap and the §6 P1 item on BLUEPRINT_COVERAGE_MAP.md.
---

# CONTENT IDEA BANK — R&D TERMINAL ROLE 5

**Status of the system as a whole: MISSING → this doc is the first blueprint.** Nothing in the vault
defined Role 5 before now. Both endpoints it wires together (RESEARCH_BANKS, CONTENT_BANKS) exist but
are themselves STATUS: UNCONFIRMED. This doc is the *architecture spec only* — no code, no live service
change. Every model, path, and threshold not already locked in a CANON doc is flagged UNCONFIRMED or
FOR HUMAN REVIEW below.

## ONE-LINE DEFINITION
Role 5 is the **score/dedup engine** that sits between the research feeder and the content library:

```
RESEARCH_BANKS  ──►  [ Role 5: score + dedup ]  ──►  CONTENT_BANKS
(raw 24/7 intake)        (Ollama on R&D Terminal)      (proven / testing / rejected library)
```

It is the missing middle. RESEARCH_BANKS already names the R&D Terminal as the 24/7 trend feeder;
CONTENT_BANKS already defines HOOK_BANK / CTA_BANK / SCRIPT_TEMPLATES / CONTENT_MAP_TEMPLATES as the
target. Neither describes how raw research becomes a scored, deduplicated, niche-filed content element.
That transform is Role 5.

---

## WHERE THIS SITS IN THE R&D TERMINAL (CANON context)
From `RD_TERMINAL_ARCHITECTURE.md` (CANON, v0.2.0): the R&D Terminal runs four CANON roles
(1 Telemetry · 2 Client Review Gateway · 3 Workflow Optimization · 4 Sandbox Investor). Role 5 is the
**new fifth role** — first appearing as MISSING in `BLUEPRINT_COVERAGE_MAP.md` §3 / §6 P1.

CANON constraints inherited from the Terminal that bind every stage below:
- **GPU: RTX 3060, 12GB VRAM.** Hard ceiling. `LOCAL_MODELS.md` (CANON): *"NEVER load both
  [qwen3:8b + qwen3:14b] simultaneously."* and `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_KEEP_ALIVE=2m`.
- **Role 5 shares one Ollama instance with Role 3 (Workflow Optimization).** Coverage map §3 marks this
  a VRAM risk; no co-load scheduling rule exists yet (that is gap §6 P14). **UNCONFIRMED.**
- **No independent internet on R&D Terminal.** `LOCAL_MODELS.md` (CANON): the Terminal reaches the
  outside world and the Engine Body Ollama only over the **direct ethernet ICS link 192.168.137.x**
  (Engine Body Ollama at `http://192.168.137.1:11434`) plus Tailscale for remote access; Syncthing
  syncs the vault. All Stage 6 boundary rules below derive from this.

---

## THE SIX STAGES

### STAGE 1 — INGESTION  (feeder: RESEARCH_BANKS)
**What:** Pull raw research the R&D Terminal already produces 24/7 and present it to the scorer as a
normalized queue of candidate content elements.

**Source — RESEARCH_BANKS.md (UNCONFIRMED), three folders:**
| Source folder | Holds | Niche-keyed? |
|---|---|---|
| `TREND_RESEARCH/` | trend findings per niche (FITNESS_TRAINER, ATHLETE, INSTAGRAM_ALGORITHM, GENERAL_CONTENT) | yes |
| `PLATFORM_INSIGHTS/` | IG algorithm updates, format changes, best practices | no (global) |
| `COMPETITOR_REFERENCES/` | what's working per niche | yes |

**Ingestion contract [UNCONFIRMED — proposed, not in any CANON doc]:** each research drop becomes one
candidate record. Proposed minimal schema (FOR HUMAN REVIEW):
```json
{
  "candidate_id": "auto",
  "source_bank": "TREND_RESEARCH | PLATFORM_INSIGHTS | COMPETITOR_REFERENCES",
  "niche": "FITNESS_TRAINER | ATHLETE | ...",
  "element_type": "hook | cta | script_template | content_map | platform_insight",
  "raw_text": "...",
  "captured_at": "ISO-8601",
  "origin_ref": "url or competitor handle [external — see Stage 6]"
}
```
- **Trigger UNCONFIRMED:** whether ingestion is a filesystem watch on the RESEARCH_BANKS folders, an
  n8n cron, or a manual kick. No vault doc specifies it. (Note: n8n WF3 RESEARCH handler is itself
  UNBUILT/THIN per coverage map §4 / §6 P8.)
- **Element typing UNCONFIRMED:** who/what assigns `element_type` (the scorer model vs an upstream
  research template). Proposed: the Stage 2 model classifies it.

### STAGE 2 — PROCESSING  (score + dedup engine)
**What:** The core transform. For each candidate: (a) **deduplicate** against what is already in
CONTENT_BANKS, and (b) **score** it so it lands in the right bucket (proven / testing / rejected).

**Model — proposed `qwen3:8b` [grounded in CANON, assignment UNCONFIRMED].**
- `LOCAL_MODELS.md` (CANON) lists `qwen3:8b` as the R&D Terminal **primary: classify, summarize,
  route (~5.2GB VRAM)** and explicitly lists *"Script matching"*, *"Take ranking (lightweight)"* and
  *"Trend research synthesis"* among locally-handled tasks — Role 5's scoring is exactly this class.
- **~5.2GB fits comfortably under the 12GB ceiling** with room for the embedding model (below) if both
  are needed. `qwen3:14b` (~10GB) would leave no headroom and would collide harder with Role 3.
- **UNCONFIRMED:** no CANON doc assigns a model to Role 5 specifically. Recommendation = `qwen3:8b`.
  FOR HUMAN REVIEW: confirm `qwen3:8b` as the Role 5 scorer, or pin a different model.

**Dedup mechanism [UNCONFIRMED]:**
- Lightweight path (no new infra): exact + fuzzy text match within the same `niche` + `element_type`,
  done by the scorer model.
- Semantic path (better, needs infra): embedding similarity. The only embedding model named anywhere
  in the vault is `nomic-embed-text` in `VECTOR_LAYER_PLAN.md` (FHR) — but that whole layer is
  **UNBUILT / orphan** (coverage map §4, §6 P11) and Qdrant is not running. **UNCONFIRMED** whether
  Role 5 dedup uses the vector layer or stays text-only for v1.
- **Dedup threshold UNCONFIRMED:** the similarity cutoff for "this is a duplicate" is not set anywhere.

**Scoring [UNCONFIRMED — no rubric exists in the vault]:**
- The score decides the destination bucket (Stage 3). Proposed inputs to a score: novelty (vs existing
  bank), niche-fit, platform-insight alignment, and (after Stage 5 exists) historical performance.
- **All score thresholds UNCONFIRMED.** There is no proven/testing/rejected numeric boundary anywhere
  in CONTENT_BANKS.md or any CANON doc. Will must set the rubric. FOR HUMAN REVIEW.
- **Proposed default routing on first pass:** a brand-new, non-duplicate, niche-matched element enters
  as **`testing`** — never directly `proven`. Promotion to `proven` happens only via Stage 5 feedback.
  (This is a proposal, not a vault rule — FOR HUMAN REVIEW.)

**VRAM discipline (CANON-derived):** `OLLAMA_NUM_PARALLEL=1` and the never-co-load rule mean Role 5
and Role 3 cannot both hold a model at once. A scheduling/priority rule is **MISSING (gap §6 P14)** and
must be written before Role 5 runs alongside Role 3. **UNCONFIRMED** — flagged, not invented here.

### STAGE 3 — STORAGE  (target: CONTENT_BANKS)
**What:** Write the scored, deduplicated element into the correct CONTENT_BANKS structure.

**Target — CONTENT_BANKS.md (UNCONFIRMED), existing structure honored exactly:**
| Bank | Structure (from CONTENT_BANKS.md) | Role 5 writes |
|---|---|---|
| `HOOK_BANK/<NICHE>/` | `hooks_proven.md`, `hooks_testing.md`, `hooks_rejected.md` | new hooks → `hooks_testing.md` by default; moved between files by Stage 5 |
| `CTA_BANK/` | by niche + funnel position (TOP / MID / BOTTOM) | scored CTAs filed by niche + funnel slot |
| `SCRIPT_TEMPLATES/` | Hook(5s) / Body / CTA / B-roll / talking-prompt variations | assembled script frameworks per client type |
| `CONTENT_MAP_TEMPLATES/` | monthly calendars: weekly reel concepts, hook+CTA rotation, funnel balance | generated/updated monthly maps per niche |

**The proven / testing / rejected tri-state is already CANON-in-structure inside CONTENT_BANKS.md**
(the HOOK_BANK explicitly has the three files). Role 5 simply populates and moves elements between
them. CTA_BANK / SCRIPT_TEMPLATES / CONTENT_MAP_TEMPLATES do **not** yet declare a proven/testing/
rejected split in CONTENT_BANKS.md — **UNCONFIRMED** whether the same tri-state applies to them.

**Physical data path [UNCONFIRMED]:** `DATABANK_ARCHITECTURE.md` (UNCONFIRMED) defines two layers —
vault = architecture (`C:\SFV_BLUEPRINT\12_DATABANKS\`), **data = `SFV_ENGINE/DATABANKS/`** ("built in
v2.x+"). The concrete drive/root for `SFV_ENGINE/DATABANKS/` is **not pinned** (no `%SFV_ROOT%` mapping
in the databank docs). Per project rule: use `%SFV_ROOT%`, never a hardcoded drive. **FOR HUMAN REVIEW:**
confirm whether the live CONTENT_BANKS data lives under `%SFV_ROOT%\DATABANKS\CONTENT_BANKS\` or a
separate `SFV_ENGINE` root, and whether R&D writes it directly or hands off to the Engine Body via
Syncthing (see Stage 6).

### STAGE 4 — RETRIEVAL  (how pre-production pulls hooks / scripts)
**What:** UGC pre-production reads from CONTENT_BANKS to fill a shoot's hooks, CTAs, and script.

**Consumer — UGC_PRE_PRODUCTION.md (CANON) + the intake app.** Coverage map §2 step 4 ("Hook/script
pull from Content Banks") is **THIN**: today the intake form has a manual Hooks field and AI assist is
*"[future] only"* — *"This is exactly the gap the Content Idea Bank (Role 5) is meant to close."*

**Proposed retrieval contract [UNCONFIRMED — closes coverage map §6 P10]:**
- Query key: `niche` (+ optional funnel position for CTAs, + client memory from CLIENT_BANKS).
- Default surface: **`proven` first, then `testing`**; `rejected` never surfaced to pre-production.
- **Client-memory join:** `CLIENT_BANKS.md` (UNCONFIRMED) holds `HOOK_MEMORY`, `PACING_MEMORY`,
  `BANNED_STYLES`, `PERFORMANCE_LOG` per client. Retrieval should *exclude* anything matching a
  client's `BANNED_STYLES` and *boost* their `HOOK_MEMORY`. **UNCONFIRMED** — CLIENT_BANKS is not yet
  wired into the intake app (coverage map §2; §6 P10).
- **Retrieval mechanism UNCONFIRMED:** whether the intake app reads the markdown banks directly, hits
  an Ollama call on the Engine Body, or queries a future vector index. No CANON doc specifies it.
- **Node note:** pre-production runs on the **Engine Body**, CONTENT_BANKS data may be authored on the
  **R&D Terminal** — so retrieval depends on the Syncthing-synced copy being current (Stage 6).

### STAGE 5 — FEEDBACK  (performance → proven / rejected promotion)
**What:** Close the loop. Real reel performance moves elements between `testing` → `proven` →
`rejected`, so the bank gets smarter over time instead of accumulating untested guesses.

**Signal source [THIN/MISSING in the vault]:**
- `CLIENT_BANKS.md` defines `PERFORMANCE_LOG: [reel results over time]` per client — the intended
  signal. But coverage map §2 step 18 marks reporting **MISSING** ("PERFORMANCE_LOG is a field name
  only") and there is no metrics pipeline. **UNCONFIRMED** what the performance signal actually is
  (saves? watch-through? Will's manual call?) and where it is recorded.
- `TRAINING_DATA` databank (`DATABANK_ARCHITECTURE.md`) captures QC approved/rejected reels — a related
  but distinct loop (QC quality, not hook performance). Gap §6 P18 (training-data automation) is the
  plumbing that would also feed this. **UNCONFIRMED** whether Role 5 feedback reuses that plumbing.

**Proposed promotion rules [UNCONFIRMED — Will must ratify, FOR HUMAN REVIEW]:**
| Transition | Proposed trigger (UNCONFIRMED thresholds) |
|---|---|
| `testing → proven` | element used in N reels that meet/exceed a performance bar |
| `testing → rejected` | element used and underperforms, or flagged in a client `BANNED_STYLES` |
| `proven → rejected` | sustained decline / platform change (PLATFORM_INSIGHTS invalidates it) |
| `rejected → testing` | manual re-test only, Will-initiated |
- **N, the performance bar, and the decline window are all UNCONFIRMED** — no numbers exist in the
  vault. Do not invent. Promotion stays a manual Will decision until ratified.
- **Authority:** consistent with the Human Approval Rule — auto-scoring may *propose* promotions, but
  `proven` is a trust tier; recommend Will confirms promotions to `proven`. FOR HUMAN REVIEW.

### STAGE 6 — NODE BOUNDARY  (no independent internet; external via Engine Body ICS)
**What:** The hard isolation rule. The R&D Terminal has **no independent internet** (CANON, multiple
docs). Every external call Role 5 needs — scraping trends, fetching competitor references, pulling
platform updates — must egress through the **Engine Body ICS host**.

**CANON-grounded boundary:**
- `LOCAL_MODELS.md` (CANON): R&D ↔ Engine over **direct ethernet ICS link `192.168.137.x`**; Engine
  Body Ollama at `http://192.168.137.1:11434`; Tailscale for remote; **Syncthing** syncs the vault;
  *"R&D terminal pushes results to a shared folder the Engine monitors."*
- `RD_TERMINAL_ARCHITECTURE.md` (CANON): the design intent is *"Engine Body stays air-gapped from the
  internet"* for Role 2 and *"all roles isolated from the Engine Body."* The Engine Body is the ICS
  gateway; the R&D Terminal is downstream of it for any outbound traffic.

**Boundary rules for Role 5:**
1. **Inbound research data** (Stage 1) arrives via the Syncthing-synced RESEARCH_BANKS folders — Role 5
   reads local synced copies, it does not crawl the web itself.
2. **Any live external fetch** Role 5 triggers (e.g. enriching a competitor reference) goes **out
   through the Engine Body ICS path**, not from the R&D Terminal directly. **UNCONFIRMED** mechanism:
   whether via n8n WF3 on the Engine Body, an Engine-side scraper, or Tavily through the Engine. No
   CANON doc wires Role 5's external calls. (Tavily key rotation is an open prerequisite — §6 P8.)
3. **Outbound results** (Stage 3 writes) land in the shared/Syncthing folder the Engine Body monitors;
   the Engine Body is the system of record. **UNCONFIRMED** whether R&D writes CONTENT_BANKS data
   directly or only proposes and the Engine commits (consistent with *"Will reviews proposals before
   Engine acts"* in LOCAL_MODELS.md).
4. **ICS failover is MISSING (gap §6 P15):** if the Engine Body (ICS host) is offline, Role 5's
   external enrichment stalls. No buffer/retry/graceful-degradation rule exists. **UNCONFIRMED** —
   Role 5 must degrade to "score local research only, queue external enrichment" but this is proposed,
   not specified.

---

## THE CONNECTIVE ENGINE (summary wiring)
```
                         R&D TERMINAL (RTX 3060, 12GB, no independent internet)
 ┌────────────────────────────────────────────────────────────────────────────────────┐
 │  RESEARCH_BANKS (synced in)        Role 5: SCORE + DEDUP            CONTENT_BANKS     │
 │  ├ TREND_RESEARCH/        ───►   ┌──────────────────────┐   ───►   ├ HOOK_BANK/<niche>│
 │  ├ PLATFORM_INSIGHTS/     ───►   │ qwen3:8b  [UNCONFIRMED│         │   proven/testing/ │
 │  └ COMPETITOR_REFERENCES/ ───►   │  assignment]          │         │   rejected        │
 │                                  │ dedup vs bank         │         ├ CTA_BANK/         │
 │   external enrich ─┐             │ score → bucket        │         ├ SCRIPT_TEMPLATES/ │
 │                    │             └──────────┬───────────┘         └ CONTENT_MAP_TMPL/ │
 └────────────────────┼────────────────────────┼──────────────────────────┬─────────────┘
                      │ (Stage 6: via Engine    │ Stage 3 write (Syncthing  │ Stage 4 retrieval
                      │  Body ICS only)         │  / Engine-committed)      ▼
              ENGINE BODY (ICS host, ────────────────────────────►  UGC PRE-PRODUCTION (Engine Body)
              internet gateway)            Stage 5 feedback ◄──── PERFORMANCE_LOG (CLIENT_BANKS) [THIN]
```
- **Forward path (build):** RESEARCH_BANKS → score/dedup → CONTENT_BANKS.
- **Pull path (consume):** CONTENT_BANKS → pre-production (Stage 4).
- **Return path (learn):** performance → promote/demote (Stage 5).
- **Boundary:** all external egress and the authoritative write go through the Engine Body (Stage 6).

---

## DEPENDENCIES & PREREQUISITES (from coverage map, not invented)
| Need | State | Source |
|---|---|---|
| RESEARCH_BANKS defined & populated | UNCONFIRMED, folders only, empty | RESEARCH_BANKS.md |
| CONTENT_BANKS defined & populated | UNCONFIRMED, structure only, "currently empty" | CONTENT_BANKS.md |
| Ollama reinstalled on R&D Terminal | **NOT reinstalled post-Win11 → fallback DEAD** | coverage map §4 |
| VRAM co-load rule (Role 3 + Role 5) | **MISSING** | coverage map §6 P14 |
| ICS-internet failover (Role 4 + Role 5) | **MISSING** | coverage map §6 P15 |
| Performance/reporting signal | **MISSING** (field name only) | coverage map §2 #18 |
| CLIENT_BANKS wired into pre-pro | **THIN** | coverage map §6 P10 |
| Vector layer (optional semantic dedup) | **UNBUILT / orphan** | coverage map §6 P11 |
| n8n WF3 RESEARCH handler (ingest trigger?) | **UNBUILT / THIN** | coverage map §6 P8 |

---

## CONSOLIDATED OPEN DECISIONS / UNCONFIRMED TABLE
| # | Item | Stage | Current state | Needs |
|---|---|---|---|---|
| 1 | Confirm `qwen3:8b` as the Role 5 scorer (vs other) | 2 | grounded in LOCAL_MODELS CANON; not assigned to Role 5 | FOR HUMAN REVIEW |
| 2 | Dedup mechanism: text-only vs vector (nomic-embed-text/Qdrant) | 2 | vector layer UNBUILT/orphan | UNCONFIRMED → decide v1 = text-only? |
| 3 | Dedup similarity threshold | 2 | no value in vault | UNCONFIRMED — Will to set |
| 4 | Scoring rubric + inputs (novelty/fit/perf weights) | 2 | no rubric exists | FOR HUMAN REVIEW |
| 5 | proven/testing/rejected numeric boundaries | 2/5 | none in vault | UNCONFIRMED — Will to set |
| 6 | "New element enters as `testing`, never direct `proven`" | 2 | proposed only | FOR HUMAN REVIEW |
| 7 | VRAM co-load scheduling rule (Role 3 ↔ Role 5) | 2 | MISSING (§6 P14) | needs separate spec |
| 8 | Ingestion trigger (folder-watch / n8n cron / manual) | 1 | unspecified | UNCONFIRMED |
| 9 | Who assigns `element_type` | 1/2 | unspecified | UNCONFIRMED |
| 10 | Does tri-state apply to CTA/SCRIPT/CONTENT_MAP banks too | 3 | only HOOK_BANK declares it | UNCONFIRMED |
| 11 | Physical data path for CONTENT_BANKS (`%SFV_ROOT%` vs SFV_ENGINE root) | 3 | not pinned | FOR HUMAN REVIEW |
| 12 | R&D writes banks directly vs proposes → Engine commits | 3/6 | LOCAL_MODELS implies propose-first | FOR HUMAN REVIEW |
| 13 | Retrieval mechanism (read markdown / Ollama / vector) | 4 | unspecified | UNCONFIRMED |
| 14 | CLIENT_BANKS join (boost HOOK_MEMORY, exclude BANNED_STYLES) | 4 | not wired (§6 P10) | UNCONFIRMED |
| 15 | Performance signal definition + where recorded | 5 | MISSING (§2 #18) | FOR HUMAN REVIEW |
| 16 | Promotion thresholds (N reels, perf bar, decline window) | 5 | none in vault | UNCONFIRMED — Will to set |
| 17 | Auto-promote vs Will-confirms `proven` | 5 | Human Approval Rule implies confirm | FOR HUMAN REVIEW |
| 18 | External-enrichment egress mechanism via Engine Body ICS | 6 | unspecified (WF3/Tavily/scraper) | UNCONFIRMED |
| 19 | ICS-offline failover / degrade behavior | 6 | MISSING (§6 P15) | needs separate spec |

**Nothing in this doc is CANON.** It is the first blueprint of Role 5 and must be ratified by Will.
Promote endpoints (RESEARCH_BANKS, CONTENT_BANKS) out of UNCONFIRMED in the same review pass so the
forward path is locked end-to-end.

---

## CONNECTED FILES
- [[BLUEPRINT_COVERAGE_MAP|Blueprint Coverage Map]]
- [[RD_TERMINAL_ARCHITECTURE|R&D Terminal Architecture]]
- [[RESEARCH_BANKS|Research Banks]]
- [[CONTENT_BANKS|Content Banks]]
- [[DATABANK_ARCHITECTURE|Databank Architecture]]
- [[CLIENT_BANKS|Client Banks]]
- [[LOCAL_MODELS|Local Models]]
- [[UGC_PRE_PRODUCTION|UGC Pre-Production]]
- [[QUALITY_CONTROL|Quality Control]]
- [[VECTOR_LAYER_PLAN|Vector Layer Plan]]
- [[RESEARCH_ROUTE_SPEC|Research Route Spec]]
- [[N8N_BLUEPRINT|n8n Blueprint]]
