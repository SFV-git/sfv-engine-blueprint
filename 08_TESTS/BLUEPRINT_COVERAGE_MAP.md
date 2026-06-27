---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
CREATED_BY: Claude Code (Blueprint Builder) + 4 parallel audit subagents — 2026-06-27
LAST_UPDATED: 2026-06-27
PURPOSE: Single consolidated proof that every workflow on BOTH nodes (Engine Body + R&D Terminal),
  down to branch-specific and one-off steps, is either represented in the vault or flagged MISSING/THIN.
  This is the STEP 1 deliverable of DIRECTIVE_BLUEPRINT_AUDIT_CONTENT_BANK.md.
METHOD: 4 read-only subagents audited in parallel — A: Production pipeline · B: UGC deep · C: R&D Terminal
  roles · D: Infra + AI layer. No live system was touched. No vault file was modified during the audit.
---

# BLUEPRINT COVERAGE MAP

**The test Will set:** *"Down to shit like Premiere Pro or weird parts used specifically for the UGC."*
If a real production step has no home in the vault structure, it is a finding here.

**STATUS legend**
- **COVERED** = a doc (ideally CANON) covers this step with adequate detail.
- **THIN** = a doc exists but is UNCONFIRMED / FHR / shallow / stale.
- **MISSING** = no vault doc covers this step.

**Headline (read this first):** The blueprint is strong on infrastructure/AI-layer *planning* and weak on
the actual **creative production craft** — there is **no video-editing (Premiere Pro) workflow doc at all**,
**no Instagram scheduling workflow**, **no Lightroom preset/catalog doc**, and **the entire UGC money
pipeline before and after the shoot (lead → brief → contract → invoice → notify → report) is unblueprinted.**
The R&D Terminal's new **Content Idea Bank (Role 5) does not exist yet** in any form. See the ranked
MASTER GAP LIST (§6) for the full priority order.

---

## 1. DOMAIN A — PRODUCTION PIPELINE COVERAGE
*(CAPTURE → INGEST → CULL → EDIT(photo) → EDIT(video) → EXPORT → DELIVER → SCHEDULE → ARCHIVE, all 9 branches)*

| Step | Branch(es) | Node | Software/Service | Vault Doc | STATUS |
|---|---|---|---|---|---|
| Shoot pre-production / planning | SFV_UGC | Engine Body | React app (planned) | UGC_PRE_PRODUCTION.md (CANON) | COVERED |
| Shoot pre-production / planning | STUDIO, EVENTS, LIVE, ATHLETICS, ARCHIVE, WORLD, 404, MYTHOLOGY | Engine/Field | none | none | MISSING |
| SD/SSD ingest | All | Engine Body | Python `ingest.py` (not built) | INGEST.md (CANON) | COVERED |
| Drive download ingest | STUDIO | Engine Body | manual → staging | INGEST.md (CANON) | COVERED |
| Phone/iPhone ingest | MYTHOLOGY, WORLD | Engine Body | manual drop | INGEST.md (CANON) | THIN |
| ExifTool metadata / FFmpeg integrity on ingest | All | Engine Body | ExifTool / FFmpeg | INGEST.md (CANON, flagged FUTURE) | THIN |
| Technical cull (blur/exposure) | All | R&D Terminal | minicpm-v:8b [INFERENCE] | CULLING.md (UNCONFIRMED) | THIN |
| Duplicate grouping | All | Engine Body | Python (not built) | CULLING.md (UNCONFIRMED) | THIN |
| QR-frame protection during cull | SFV_EVENTS | Engine Body | manual discipline | EVENTS_ZENFOLIO_DELIVERY.md (FHR) | THIN |
| Creative selects (how Will culls in LR) | All | Will | Lightroom Classic [INFERENCE] | none | MISSING |
| Lightroom batch edit + sync preset | STUDIO | Engine Body | Lightroom Classic | SFV_STUDIO.md (CANON) + EXPORT.md (UNCONFIRMED) | THIN |
| Lightroom edit | EVENTS, ARCHIVE | Engine Body | Lightroom Classic | EXPORT.md (UNCONFIRMED) | THIN |
| Lightroom edit | LIVE, ATHLETICS, WORLD, 404, MYTHOLOGY | Engine Body | Lightroom Classic [INFERENCE] | none | MISSING |
| Per-branch LR catalog / preset management | All | Engine Body | Lightroom Classic | none | MISSING |
| **Video / Reel edit** | **UGC, LIVE, ARCHIVE, ATHLETICS, EVENTS, STUDIO** | **Engine Body** | **Premiere Pro** | **NONE** | **MISSING** |
| AI video transcription | UGC (primary) | R&D Terminal | Whisper via n8n MEDIA | MEDIA_PIPELINE.md (FHR) | THIN |
| Photo export (full res, social specs) | STUDIO, EVENTS, ARCHIVE | Engine Body | Lightroom Classic | EXPORT.md (UNCONFIRMED, specs TBD) | THIN |
| Video/Reel export | All | Engine Body | Premiere Pro + FFmpeg | EXPORT.md (specs TBD) | MISSING |
| Naming on export | All | Engine Body | Python/manual | NAMING_CONVENTIONS.md (CANON) | COVERED |
| Pixieset gallery delivery | STUDIO | Engine Body | Pixieset | DELIVERY.md (UNCONFIRMED) + SFV_STUDIO.md | THIN |
| Zenfolio QR delivery | EVENTS | Engine Body | Zenfolio Sports&Events | EVENTS_ZENFOLIO_DELIVERY.md (FHR, 5 open items) | THIN |
| Client delivery | UGC | Engine Body | WeTransfer (stop-gap) | DELIVERY.md (UNCONFIRMED) | MISSING |
| Direct-to-IG (no client) | MYTHOLOGY, ATHLETICS, WORLD, 404, ARCHIVE | — | — | DELIVERY.md | COVERED |
| Instagram scheduling | all 8 non-MYTHOLOGY branches | Engine Body | UNCONFIRMED (Later? Buffer?) | none | MISSING |
| Caption system | All | Engine Body | manual/engine | NAMING_CONVENTIONS.md (CANON) | COVERED |
| Archive ACTIVE→WARM | All | Engine Body | Python (planned) | ARCHIVE.md (UNCONFIRMED) | THIN |
| Archive WARM→COLD (Porsche SSD) | All | Engine Body | Python (planned) | ARCHIVE.md (UNCONFIRMED) | MISSING (SSD blocked) |
| Archive index structure | All | Engine Body | TBD | ARCHIVE.md (PENDING) | MISSING |
| Outputs retention/pruning | engine automation | Engine Body | Python (planned) | OUTPUTS_RETENTION.md (FHR) | THIN |

**Domain A notable contradictions/flags:**
- `TOOL_STATUS.md` says n8n = FUTURE; reality is n8n v2.22.5 LIVE → **TOOL_STATUS.md is stale.**
- Morning Walk / Shamar Lightroom recipe (Adaptive Portrait preset, AI-mask sync, Generative Remove,
  sRGB q80–85 2560px) is **battle-tested in practice but not in the vault** (per MISSING_REFERENCED_FILES.md §3).
- `SFV_EVENTS.md` (CANON) still says delivery = "Pixieset or different? UNCONFIRMED" while the Zenfolio
  decision is locked elsewhere — branch doc contradicts the operational decision.

---

## 2. DOMAIN B — UGC DEEP COVERAGE (Will's named priority)
*(lead → brief → pre-pro → shoot → edit → QC → delivery → client memory → reporting)*

| Step | Node | Software/Tool | Vault Doc | STATUS |
|---|---|---|---|---|
| 1. Lead intake / CRM | Engine Body | none documented | none | MISSING |
| 2. Brief / proposal / contract | Engine Body | none documented | none | MISSING |
| 3. Pre-production shoot intake | Engine Body | React app (not built) | UGC_PRE_PRODUCTION.md (CANON) | COVERED |
| 4. Hook/script pull from Content Banks | Engine Body | React app + [future Ollama] | CONTENT_BANKS.md (UNCONFIRMED) | THIN |
| 5. Client-memory pull | Engine Body | clients.json | CLIENT_BANKS.md (UNCONFIRMED) | THIN |
| 6. Shoot execution | Field/Engine | camera gear | UGC_PRE_PRODUCTION.md | THIN |
| 7. Media ingest (post-shoot) | Engine Body | Python ingest.py | INGEST.md (CANON) | COVERED |
| 8. **Video editing — reels** | **Engine Body** | **Premiere Pro (CapCut never mentioned; Aditor.ai RESEARCHING)** | **none** | **MISSING** |
| 9. Caption / subtitle generation | Engine/R&D | Captions app (RESEARCHING); Whisper (approved, not installed) | TOOL_STATUS.md | THIN |
| 10. QC — AI pre-audit | R&D Terminal | Ollama/Qwen3 [INFERENCE] | QUALITY_CONTROL.md (UNCONFIRMED) | THIN |
| 11. QC — auto-fix | R&D Terminal | none specified | QUALITY_CONTROL.md | MISSING |
| 12. QC — Claude API final layer | Engine Body | Claude API (Sonnet) | QUALITY_CONTROL.md + CLAUDE_API.md | THIN |
| 13. Will final review | Engine Body | manual | QUALITY_CONTROL.md + SFV_UGC.md | COVERED |
| 14. Training-data logging | Engine/R&D | manual/automated? | TRAINING_DATA.md (UNCONFIRMED) | THIN |
| 15. Client delivery | Engine Body | WeTransfer (temp) | DELIVERY.md (UNCONFIRMED) | THIN |
| 16. Client notification | Engine Body | none | DELIVERY.md | MISSING |
| 17. Client-memory update (post-delivery) | Engine Body | manual → clients.json | CLIENT_BANKS.md (UNCONFIRMED) | THIN |
| 18. Performance / reporting | Engine Body | none (PERFORMANCE_LOG is a field name only) | CLIENT_BANKS.md | MISSING |
| 19. Invoicing / payment | Engine Body | none documented | none | MISSING |
| 20. UGC IG scheduling (own account, Lvl 6.5) | Engine Body | Later/Buffer (RESEARCHING) | DELIVERY.md / INTEGRATIONS.md | THIN |

**Domain B answers to Will's specific questions:**
- *What edits UGC video?* Premiere Pro is the only editor in the stack; **no UGC edit workflow doc exists.**
  Whether CapCut/Aditor.ai supplement it is undecided. This is the single biggest UGC gap.
- *Is CLIENT_BANKS wired into pre-pro?* Only conceptually — rich memory fields (HOOK_MEMORY, PACING_MEMORY,
  BANNED_STYLES, PERFORMANCE_LOG) are not mapped into the intake app, and CLIENT_BANKS is UNCONFIRMED.
- *Is there a UGC QC checklist?* No formal pass/fail checklist, thresholds, tool, or output format — just
  7 bullet categories.
- *How does pre-pro pull from CONTENT_BANKS?* It doesn't yet — manual Hooks field; AI assist is [future] only.
  **This is exactly the gap the Content Idea Bank (Role 5) is meant to close.**

---

## 3. DOMAIN C — R&D TERMINAL ROLE COVERAGE
*(4 CANON roles + new Role 5; 12GB VRAM ceiling; NO independent internet — external calls via Engine Body ICS)*

| Role | Inputs | Outputs | Software | Data Location | ICS dep? | VRAM risk? | Doc | STATUS |
|---|---|---|---|---|---|---|---|---|
| 1 — Telemetry dashboard | Engine Body telemetry JSON over SMB/Tailscale | Streamlit/React dashboard | Python+Streamlit OR React (undecided); windows_exporter | D:\SFV_ACTIVE\LOGS\TELEMETRY\ (read) | No | No | RD_TERMINAL_ARCHITECTURE.md (CANON) | THIN |
| 2 — Client review gateway | client browser; assets from Engine Body D:\ | client review UI; cached assets | nginx/Caddy + React/Next; Docker | R&D local cache (path undefined) | **Yes — inbound path UNDEFINED** | No | RD_TERMINAL_ARCHITECTURE.md (CANON) | THIN |
| 3 — Workflow optimization engine | telemetry JSON | text recommendations | Ollama qwen3:8b/14b | reads Engine Body telemetry; output → TASK_QUEUE.md (**LEGACY/stale**) | No | **Yes — shares Ollama w/ Role 5** | RD_TERMINAL_ARCHITECTURE.md + LOCAL_MODELS.md (CANON) | THIN |
| 4 — Sandbox investor | Polymarket + Alpaca APIs | trade logs (container-internal) | Docker + Python | container-only, no vault write | **Yes — trading APIs via ICS, no failover** | No | RD_TERMINAL_ARCHITECTURE.md (CANON) | THIN |
| **5 — Content Idea Bank (NEW)** | **[MISSING]** | **[MISSING]** | **[MISSING]** | **[MISSING]** | **Yes — scraping via ICS** | **Yes [INFERENCE]** | **none** | **MISSING** |

**Role 5 substrate that already exists (to be connected):**
- **RESEARCH_BANKS.md** (UNCONFIRMED) — names R&D Terminal as the 24/7 trend feeder; folders for
  TREND_RESEARCH / PLATFORM_INSIGHTS / COMPETITOR_REFERENCES. → **the INPUT feeder.**
- **CONTENT_BANKS.md** (UNCONFIRMED) — HOOK_BANK (per niche, proven/testing/rejected), CTA_BANK,
  SCRIPT_TEMPLATES, CONTENT_MAP_TEMPLATES; currently empty. → **the OUTPUT target.**
- **DATABANK_ARCHITECTURE.md** (UNCONFIRMED) — two-layer model (vault=architecture, SFV_ENGINE/DATABANKS/=data).
- The connective engine RESEARCH_BANKS → (score/dedup) → CONTENT_BANKS is the entire gap Role 5 fills.

---

## 4. DOMAIN D — INFRASTRUCTURE + AI-LAYER COVERAGE

| Subsystem | Node | Software/Service/MCP | Doc | Live/Planned/Unbuilt | STATUS |
|---|---|---|---|---|---|
| n8n WF1 queue processor | A | n8n v2.22.5 | N8N_BLUEPRINT.md + workflow1 JSON | LIVE (confidence-fix re-import pending) | THIN |
| n8n WF2 pre-warm cron | A | n8n | N8N_BLUEPRINT.md + workflow2 JSON | LIVE | COVERED |
| n8n WF3 RESEARCH handler | A | n8n + Tavily | RESEARCH_ROUTE_SPEC.md + N8N_BLUEPRINT.md (FHR) | UNBUILT (specs slightly contradict) | THIN |
| n8n WF4 output monitor | A | n8n | N8N_BLUEPRINT.md + workflow4 JSON | LIVE (had process.env bug, fixed 06-28) | COVERED |
| n8n WF5 blueprint sync | A | n8n | N8N_BLUEPRINT.md only | UNBUILT (name collides w/ a validation WF5) | MISSING |
| Ollama — Engine Body | A | qwen3:14b, qwen2.5-coder:7b, minicpm-v:8b | LOCAL_MODELS.md (CANON) | LIVE | COVERED |
| Ollama — R&D Terminal | B | qwen3:14b (+8b planned) | LOCAL_MODELS.md (CANON) | **NOT reinstalled post-Win11 → fallback DEAD** | THIN |
| Model routing | A | n8n logic | MODEL_ROUTING.md (CANON) | speced + partly live | COVERED |
| PostgreSQL migration | A | PostgreSQL 15 | POSTGRES_MIGRATION.md (FHR) | **PENDING — n8n still SQLite** | THIN |
| Docker | A | Docker Desktop (WSL2) | DOCKER_INSTALL_CHECKLIST.md (CANON) | **APPROVED, not installed — blocks 5+ items** | THIN |
| Open WebUI | A | Docker (3000) | OPEN_WEBUI_SPEC.md (FHR) | UNBUILT (blocked by Docker) | THIN |
| n8n-MCP server | A | Docker czlonkowski/n8n-mcp | N8N_MCP_SPEC.md (CANON) | UNBUILT (blocked by Docker+PG) | THIN |
| Syncthing | both | Syncthing | **none dedicated** (inline only) | LIVE | MISSING |
| Tailscale | both | Tailscale | **none dedicated** (status contradicted) | ACTIVE [INFERENCE] | MISSING |
| Hermes Agent | A+B | Hermes daemon (NousResearch) | HERMES_INTEGRATION.md (FHR) | UNBUILT (pending A1 decision) | THIN |
| Vector layer | A | Qdrant + nomic-embed-text | VECTOR_LAYER_PLAN.md (FHR) | **UNBUILT — orphan plan, no consumer wired** | THIN |
| Monitoring stack | A | Prometheus + Grafana | MONITORING_STACK.md (FHR) | UNBUILT (blocked by Docker) | THIN |
| windows_exporter | both | windows_exporter (9182) | MONITORING_STACK.md (FHR) | A: installed; B: unknown post-rebuild | THIN |
| Redis queue mode | A | Redis Docker | CONCURRENCY_QUEUE_SPEC.md (CANON) §5 | FUTURE (blocked by PG) | THIN |
| Secrets / key mgmt | A | n8n_env.ps1 + Bitwarden | SECRETS_POLICY.md (CANON) | PARTIAL — **Tavily key plaintext, rotation pending** | THIN |
| Disaster recovery | both | pg_dump, backup_n8n.ps1, Git, Robocopy | DISASTER_RECOVERY.md (FHR) | PARTIAL — **n8n backup NOT scheduled** | THIN |
| Failover / watchdog | A | watchdog.ps1 | FAILOVER_MODEL.md (FHR) | PARTIAL — manual window, not Scheduled Task | THIN |
| Confidence logic | A | n8n WF1 | CONFIDENCE_LOGIC.md (CANON) | doc CANON, live re-import pending | THIN |
| Output validation | A | n8n WF1 | OUTPUT_VALIDATION.md (CANON) | speced, not implemented in WF1 | THIN |
| Prompt versioning | A | OLLAMA_PROMPTS/ | PROMPT_VERSIONING.md (CANON) | speced, not baselined | THIN |
| Cost ceiling / routing | A | COST_ALERTS.md | COST_CEILING_POLICY.md (FHR) / COST_ROUTING.md (CANON) | alert-only | THIN/COVERED |
| Gemini n8n direct | A | n8n HTTP + AI Studio API | GEMINI_INTEGRATION.md (FHR) | NOT built (no key) | THIN |
| Rate limits | A+cloud | all services | RATE_LIMITS.md (CANON) | COVERED ([INFERENCE] values) | COVERED |
| Job envelope schema | A | n8n WF1 | JOB_ENVELOPE_SPEC.md (FHR) | live in WF1, needs CANON promo | THIN |
| Concurrency/priority queue | A | n8n WF1 | CONCURRENCY_QUEUE_SPEC.md (CANON) | speced, not implemented | THIN |

---

## 5. COVERAGE SCORECARD (counts)

| Domain | COVERED | THIN | MISSING |
|---|---|---|---|
| A — Production pipeline | 5 | 11 | 9 |
| B — UGC lifecycle (20 steps) | 4 | 9 | 7 |
| C — R&D Terminal roles (5) | 0 | 4 | 1 (whole Role 5) |
| D — Infra + AI layer (31) | 6 | 19 | 6 |

*Interpretation:* the engine room (infra/AI) is mostly **planned-but-THIN** (docs exist, execution pending).
The **craft layer (video edit, scheduling, Lightroom, UGC business pipeline) is where the true MISSING holes are.**

---

## 6. MASTER GAP LIST — RANKED (this is the build-the-blueprint backlog)

> Ranking weights: (1) revenue impact, (2) "no doc at all" beats "thin doc", (3) Will's stated priority
> (UGC + Content Idea Bank), (4) how many other things it unblocks. Each is the seed for one FHR doc.

**P1 — Content Idea Bank (R&D Terminal Role 5)** — *entirely MISSING.* No `CONTENT_IDEA_BANK.md`; all 6
stages (ingestion, processing, storage, retrieval, feedback, node boundary) undefined. Will's headline
deliverable. → handled in STEP 2 P1. Depends on RESEARCH_BANKS/CONTENT_BANKS (both UNCONFIRMED).

**P2 — Premiere Pro / video-edit workflow** — *MISSING entirely.* Affects UGC (revenue), LIVE, ARCHIVE,
ATHLETICS, EVENTS, STUDIO. Needed: `04_WORKFLOWS/VIDEO_EDIT_WORKFLOW.md` — per-branch edit approach, reel
assembly, audio sync, color, caption hand-off, export preset → FFmpeg/Premiere encoder. Tool confirmation
(Premiere vs CapCut vs Aditor.ai for UGC reels) is itself an open decision.

**P3 — UGC business pipeline (lead → brief → contract → invoice → notify → report)** — *MISSING, 5 distinct
holes.* The money branch has no blueprint for converting/serving/billing clients. Needed: `UGC_LEAD_INTAKE.md`
(CRM tool), `UGC_BRIEF.md` (brief/proposal/contract), `UGC_INVOICING.md` (payment), client notification +
`UGC_REPORTING.md` (performance). Tool selections (CRM, contract, payment, analytics) are open decisions.

**P4 — Instagram scheduling workflow** — *MISSING for all 8 non-MYTHOLOGY branches.* Tool undecided
(Later vs Buffer). Needed: scheduling-tool decision (FHR) + `04_WORKFLOWS/SCHEDULING_WORKFLOW.md` with
per-branch timing rules, caption insertion, n8n integration.

**P5 — Lightroom preset + catalog per-branch workflow** — *MISSING as a doc; battle-tested in practice.*
Needed: `04_WORKFLOWS/LIGHTROOM_WORKFLOW.md` — per-branch presets, catalog structure, sync approach,
confirmed export specs (promote the Morning Walk/Shamar recipe). Resolves the EXPORT.md "specs TBD" hole too.

**P6 — UGC client delivery platform** — *MISSING/UNCONFIRMED.* Revenue branch on WeTransfer stop-gap.
Needed: platform decision (portal vs Drive vs Pixieset) + `UGC_DELIVERY.md` + notification path.

**P7 — Promote EVENTS_ZENFOLIO_DELIVERY.md to CANON** — *THIN (5 open items).* Resolve: Zenfolio Advanced
plan caps/pricing, QR card stock source, QR export format, per-day event template, 3-laptops/1-account
concurrency. Then promote, and fix the SFV_EVENTS.md delivery contradiction.

**P8 — WF3 RESEARCH handler structure** — *THIN/UNBUILT.* Reconcile the RESEARCH_ROUTE_SPEC vs N8N_BLUEPRINT
trigger-mechanism contradiction, then finalize the WF3 structural spec. Tavily key rotation is a prerequisite.

**P9 — QC system spec (UGC)** — *THIN→MISSING.* Needed: `QC_CHECKLIST.md` — per-item pass/fail thresholds,
named Ollama model + prompt, output format, escalation trigger to Claude API, and the auto-fix scope.

**P10 — CONTENT_BANKS / CLIENT_BANKS wiring into pre-production** — *THIN.* Map CLIENT_BANKS memory fields
into the intake app schema; define how hooks/scripts surface in the form. Overlaps with Role 5 retrieval.

**P11 — Vector layer wiring** — *THIN/orphan.* Add a "FUTURE — Phase 2" header + prerequisite chain
(Docker → Qdrant → nomic-embed-text → vault_watcher extension → WF1 RAG). Evaluate it as Role 5 storage.

**P12 — Syncthing + Tailscale dedicated specs** — *MISSING docs for live tools.* Needed:
`SYNCTHING_SPEC.md` (folders, version history, conflict handling) and `TAILSCALE_SPEC.md` (isolation rule,
node IPs, remote policy); resolve the INTEGRATIONS.md UNCONFIRMED contradiction.

**P13 — Role 2 client inbound network path** — *MISSING.* R&D Terminal has no independent internet; define
how external clients reach the review gateway (ICS port-forward vs Tailscale share). Blocks Role 2.

**P14 — VRAM scheduling rule (Roles 3 + 5)** — *MISSING.* Define an Ollama single-large-model-at-a-time
scheduling/priority rule for the 12GB ceiling so Role 3 and Role 5 never co-load.

**P15 — ICS-internet failover (Roles 4 + 5)** — *MISSING.* Define buffer/retry/graceful-degradation for
when Engine Body (the ICS host) is offline and R&D external calls stall.

**P16 — Shoot capture checklists** — *MISSING for 8/9 branches.* A single `SHOOT_CHECKLIST.md` with
branch sections (STUDIO 50+ models, EVENTS on-site setup, ATHLETICS) would close it cheaply.

**P17 — ARCHIVE.md completion** — *THIN, cold storage BLOCKED.* Resolve Porsche SSD filesystem issue,
set ACTIVE→WARM→COLD timing thresholds, define archive index, promote to CANON.

**P18 — Training-data automation** — *THIN.* Define the trigger (Python/n8n) that moves files to
QC_APPROVED/QC_REJECTED on Will's decision and logs the outcome — the feedback-loop plumbing for Role 5.

**Standing prerequisites that gate several of the above (not gaps, but blockers):**
PostgreSQL migration · Docker install · WF1 confidence-fix re-import · Tavily key rotation · n8n backup
scheduling · Ollama Node B reinstall. (All tracked in CRITICAL_PATH.md / SESSION_STATE.md.)

---

## 7. WHAT THIS PROVES
Every production step on both nodes — including the "weird" ones Will called out (Premiere Pro, UGC-specific
tooling, QR-frame culling, the Zenfolio multi-laptop event flow) — now has an explicit COVERED/THIN/MISSING
verdict and a vault home or a flagged gap. Nothing in the walked lifecycle is unaccounted for. The 18-item
ranked MASTER GAP LIST (§6) is the backlog that STEP 2 works, starting with the Content Idea Bank (P1).

---

## CONNECTED FILES
- [[DIRECTIVE_BLUEPRINT_AUDIT_CONTENT_BANK|Directive — Audit + Content Idea Bank]]
- [[CONTENT_IDEA_BANK|Content Idea Bank (Role 5)]]
- [[RD_TERMINAL_ARCHITECTURE|R&D Terminal Architecture]]
- [[TOOL_RESEARCH|Tool Research]]
- [[UGC_PRE_PRODUCTION|UGC Pre-Production]]
- [[CONTENT_BANKS|Content Banks]]
- [[RESEARCH_BANKS|Research Banks]]
- [[CLIENT_BANKS|Client Banks]]
- [[INGEST|Ingest]]
- [[CULLING|Culling]]
- [[EXPORT|Export]]
- [[DELIVERY|Delivery]]
- [[EVENTS_ZENFOLIO_DELIVERY|Events Zenfolio Delivery]]
- [[ARCHIVE|Archive]]
- [[QUALITY_CONTROL|Quality Control]]
- [[VECTOR_LAYER_PLAN|Vector Layer Plan]]
- [[RESEARCH_ROUTE_SPEC|Research Route Spec]]
- [[N8N_BLUEPRINT|n8n Blueprint]]
- [[CRITICAL_PATH|Critical Path]]
- [[SESSION_STATE|Session State]]
