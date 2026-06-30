---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
CREATED_BY: Claude Chat (Blueprint Builder) — 2026-06-27 session
PURPOSE: Directive for Claude Code (+ subagents) to (1) audit the blueprint for completeness so NO part of
  the Engine Body or R&D Terminal workflow is missing from the structure, then (2) research + flesh out the
  gaps — with first focus on the CONTENT IDEA BANK running on the R&D Terminal.
BLUEPRINT LOCK: This is planning/structure work. Produce FOR HUMAN REVIEW docs only. NO CANON promotion.
  NO building. NO live-system changes. Will ratifies everything.
---

# DIRECTIVE — BLUEPRINT COMPLETENESS AUDIT + CONTENT IDEA BANK BUILD-OUT

## WHY THIS EXISTS (Will's intent, verbatim intent)
Will does NOT want to reach the building stage and discover whole subsystems were never blueprinted.
Before any code is written, the blueprint STRUCTURE must account for every workflow on both nodes —
down to the small/branch-specific pieces (e.g. Premiere Pro steps, the specific tools used only for UGC,
weird one-off parts). This is a two-step job:

- **STEP 1 — COMPLETENESS AUDIT (do this FIRST).** Prove that every part of the Engine Body and R&D
  Terminal workflows is represented somewhere in the vault structure. Find what's missing. Output a gap map.
- **STEP 2 — RESEARCH + FLESH OUT.** For the gaps (starting with the Content Idea Bank on R&D Terminal),
  research the services/software/MCPs that could fill them, record findings, and write the structural docs.

The headline deliverable Will named: figure out **how the Content Idea Bank runs on the R&D Terminal** —
what feeds it, what processes it, what software/service/MCP each stage uses, and where its data lives.

---

## GROUND TRUTH ALREADY ESTABLISHED (do not re-derive — read these, build on them)

### The two nodes (CANON)
- **Engine Body** (Ryzen 9 9900X / RTX 5080 / 32→64GB / Win11): the WORKER. Production: ingest, Lightroom,
  Premiere, exports, n8n, Ollama, Postgres, Claude Code. Stays heads-down. Air-gapped from internet where possible.
- **R&D Terminal** (RTX 3060 / 16GB / 24/7 / Win11): the SENTINEL / OBSERVER. Never touches production.
  Routes internet via Engine Body ICS. See `05_AI_LAYER/RD_TERMINAL_ARCHITECTURE.md` (CANON).

### R&D Terminal already has 4 CANON roles (Proposal 007, approved)
1. Telemetry reader + workflow dashboard (Streamlit/React)
2. Client review gateway (reverse proxy, clients never hit Engine Body)
3. Workflow optimization engine (Ollama agent reading telemetry)
4. Sandbox investor (isolated Docker trading container)
**→ The Content Idea Bank is a NEW 5th role.** It fits the R&D Terminal philosophy perfectly: continuous
background trend-scraping + idea generation + hook scoring is exactly the kind of always-on, non-production
work that must NOT steal Engine Body cycles. Slot it in as Role 5 WITHOUT breaking node isolation.

### Databank substrate already exists (UNCONFIRMED, thin)
`12_DATABANKS/` has architecture for 6 bank types: CONTENT, TASTE, CLIENT, BRAND, RESEARCH, TRAINING.
Two layers defined: vault holds ARCHITECTURE docs; `SFV_ENGINE/DATABANKS/` holds ACTUAL DATA (v2.x+).
- `CONTENT_BANKS.md` = hooks/CTAs/scripts/content-maps, but it's STATIC, UGC-only, folder-of-templates.
- `RESEARCH_BANKS.md` is explicitly "fed by R&D terminal continuous research (24/7)" — already names the
  R&D Terminal as the feeder. **The Content Idea Bank is the ACTIVE engine that connects RESEARCH_BANKS
  (input/trends) → CONTENT_BANKS (output/usable ideas). That connective tissue is the gap.**

### Hard constraints to respect
- R&D Terminal has NO independent internet — every external API/scrape call routes through Engine Body ICS.
  (This is a real dependency: if Engine Body is down, R&D Terminal research stalls. Account for it.)
- 12GB VRAM ceiling on R&D Terminal. Never load two large models at once (qwen3:8b + qwen3:14b = over).
- Blueprint Lock: structure before build. Long-term correctness over deadlines.
- Tavily key is currently PLAINTEXT in n8n_env.ps1 and must be rotated before any new web-search wiring —
  flag this as a prerequisite, do not bake the live key into any new doc.

---

## STEP 1 — COMPLETENESS AUDIT (subagents work in parallel, one domain each)

**Goal:** A single gap-map doc proving every workflow on both nodes is represented in the vault — or
flagged as missing. The test Will set: "down to shit like Premiere Pro or weird parts used specifically
for the UGC." If a real production step has no home in the structure, that's a finding.

**Method:** Walk each branch and each node end-to-end as an ACTUAL workflow (capture → ingest → cull →
edit → export → deliver → schedule → archive), and for every step name: (a) which node runs it, (b) which
software/service does it, (c) which vault doc covers it, (d) MISSING if none. Do the same for every R&D
Terminal role and every infrastructure/AI-layer subsystem.

**Suggested subagent split (parallelizable — run as separate subagents):**
- **Subagent A — Production pipeline coverage.** Walk INGEST → CULLING → EXPORT → DELIVERY → ARCHIVE
  (04_WORKFLOWS) for each of the 9 branches. Confirm every tool is named and doc'd: Lightroom (which
  preset per branch), Premiere Pro (UGC/LIVE video — IS THERE A PREMIERE WORKFLOW DOC? likely MISSING),
  Pixieset (studio/portrait), Zenfolio (events), Later (scheduling). Output: per-branch step→tool→doc table.
- **Subagent B — UGC deep coverage (Will's named priority).** UGC is the money branch and most tool-heavy.
  Walk the FULL UGC lifecycle: lead → brief → pre-production (UGC_PRE_PRODUCTION.md exists) → shoot →
  edit (Premiere? CapCut? what exactly) → QC → delivery → client memory. Name every tool incl. the weird
  UGC-specific ones. Cross-check against CONTENT_BANKS + CLIENT_BANKS. Output: UGC tool+step inventory + gaps.
- **Subagent C — R&D Terminal role coverage.** Confirm all 5 roles (4 existing + new Content Idea Bank)
  have: defined inputs, defined outputs, named software, and a data-location. Flag the ICS-internet
  dependency for each role that needs external calls. Output: R&D Terminal role→software→data table + the
  Role 5 stub for Step 2 to expand.
- **Subagent D — Infra + AI-layer coverage.** Walk 03_INFRASTRUCTURE + 05_AI_LAYER. Confirm every live
  + planned subsystem has a doc and a clear owner-node: n8n (WF1/2/3/4 — WF3 still unbuilt), Ollama models,
  Postgres, Docker (uninstalled), Syncthing, Tailscale, Hermes (pending A1), MCP servers, vector layer
  (VECTOR_LAYER_PLAN exists — is it wired to anything?), monitoring. Output: subsystem→node→status→doc table.

**STEP 1 DELIVERABLE:** `08_TESTS/BLUEPRINT_COVERAGE_MAP.md` (FOR HUMAN REVIEW) — one consolidated matrix:
every workflow step / subsystem × {node, software/service/MCP, vault doc, STATUS: COVERED / THIN / MISSING}.
Plus a ranked "MISSING/THIN — needs blueprinting" list. THIS is the artifact that proves nothing was forgotten.

---

## STEP 2 — RESEARCH + FLESH OUT (Content Idea Bank first, then other gaps)

**Priority 1: CONTENT IDEA BANK on R&D Terminal (R&D Terminal Role 5).**
Write a new doc `05_AI_LAYER/CONTENT_IDEA_BANK.md` (FOR HUMAN REVIEW) that fully specs it as a pipeline.
At minimum, answer for EACH stage — INPUT, PROCESS, OUTPUT — what software/service/MCP runs it and where
data lands:

1. **INGESTION (what feeds ideas in).** Trend sources: which platforms (TikTok/IG/YT trends, competitor
   accounts, are.na boards, Reddit niches)? Which service pulls them — Tavily? Apify? a scraping MCP? RSS?
   Manual Perplexity drops? Define the feed list + the tool per feed. Respect ICS-internet dependency.
2. **PROCESSING (how raw trends → scored ideas).** Local Ollama on R&D Terminal classifies/scores hooks by
   niche + funnel position (ties to existing HOOK_BANK / CTA_BANK structure). Define the model (12GB-safe),
   the scoring rubric, dedup against existing banks, and the n8n/agent that orchestrates it.
3. **STORAGE (where it lives).** Maps to the two-layer databank model: architecture in vault, data in
   `SFV_ENGINE/DATABANKS/`. Decide: flat markdown banks (current) vs a real DB (Postgres? SQLite? a vector
   store for semantic idea-retrieval — VECTOR_LAYER_PLAN already exists, evaluate using it). Recommend one.
4. **RETRIEVAL (how production pulls ideas out).** When a UGC shoot is being planned (UGC_PRE_PRODUCTION
   app), how does it query the bank for relevant hooks/scripts? API? MCP? direct file read? Define it.
5. **FEEDBACK LOOP (what makes it improve).** TRAINING_DATA bank already exists (approved/rejected reels).
   Define how QC outcomes feed back to re-score hooks (winning hooks float up, losers archived).
6. **NODE BOUNDARY.** Make explicit what runs on R&D Terminal (scraping, scoring, storage, 24/7) vs what
   Engine Body touches (only pulls finished ideas at pre-production time). Preserve isolation.

**Research mandate for Priority 1:** Actively research current services/MCPs that fit — don't just use
what's already in the stack. Candidates to evaluate (confirm they're real + current, find others):
Apify, Browse AI, social-scraping MCPs, RSS aggregators, are.na API, n8n community nodes for social,
vector DBs (Qdrant/Chroma/pgvector), and any "trend intelligence" APIs. Record findings in
`10_REFERENCES/TOOL_RESEARCH.md` (append) with: service, what it does, cost, fit, ICS-compatibility,
verdict. Cite sources. Flag anything that needs a paid plan or a key.

**Priority 2+: the other MISSING/THIN gaps** surfaced by Step 1's coverage map, worked in ranked order
(likely: Premiere Pro / video-edit workflow doc, any UGC-specific tool with no doc, WF3 RESEARCH handler
structure, vector layer wiring). One FOR HUMAN REVIEW doc per gap, same INPUT/PROCESS/OUTPUT + software
+ data-location discipline.

---

## RULES FOR THIS DIRECTIVE (enforce across all subagents)
- FOR HUMAN REVIEW status on everything. NO CANON. NO building. NO live n8n/Ollama/Postgres changes.
- Label CANON / UNCONFIRMED / INFERENCE / FOR HUMAN REVIEW inside docs as appropriate.
- No invention of facts about services — research and cite. If unverified, label it UNCONFIRMED.
- Respect node isolation (Engine Body = worker, R&D Terminal = observer) in every design.
- Respect the 12GB VRAM ceiling and the ICS-internet dependency in every R&D Terminal design.
- Do NOT bake the live Tavily key into any doc; flag key-rotation as a prerequisite.
- Every new doc gets a CONNECTED FILES section wikilinking its neighbors.
- End by updating SESSION_STATE.md with a session block + writing a handoff for the next session.

## DELIVERABLES CHECKLIST (what "done" looks like)
- [ ] `08_TESTS/BLUEPRINT_COVERAGE_MAP.md` — the completeness matrix + ranked gap list (STEP 1)
- [ ] `05_AI_LAYER/CONTENT_IDEA_BANK.md` — full R&D Terminal Role 5 pipeline spec (STEP 2 P1)
- [ ] `10_REFERENCES/TOOL_RESEARCH.md` — appended with researched services + verdicts + sources
- [ ] One FOR HUMAN REVIEW doc per remaining ranked gap (STEP 2 P2+)
- [ ] `RD_TERMINAL_ARCHITECTURE.md` — proposed Role 5 addition noted (as FHR edit, NOT a CANON rewrite)
- [ ] SESSION_STATE block + next-session handoff written

## CONNECTED FILES
- [[SESSION_STATE|Session State]]
- [[DASHBOARD|Dashboard]]
