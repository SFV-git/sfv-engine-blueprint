---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-30
---

# CHANGELOG

## 2026-06-30 — P7-ZENFOLIO-CANON: EVENTS_ZENFOLIO_DELIVERY open items resolved → CANON-ready (Claude Code)
- `04_WORKFLOWS/EVENTS_ZENFOLIO_DELIVERY.md` v0.1.0 → v0.2.0 (STATUS unchanged: FOR HUMAN REVIEW — **not** self-promoted per canon-control rule).
- Resolved the 5 open verification items to honest dispositions instead of invented values: items 1/3/5 (Zenfolio Advanced caps/pricing, QR export format, 3-laptop/1-account concurrency) = **UNCONFIRMED (external vendor facts)**; item 2 (QR card stock/source) = **UNCONFIRMED/MISSING**; item 4 (per-day event template) = **MISSING (build artifact)**. Grep + MISSING_REFERENCED_FILES.md confirm the vault records no value for any of them.
- Added a READY-TO-PROMOTE NOTE: operational core is CANON-ready; none of the open items block the workflow logic (only capacity/cost/setup planning).
- **Flagged (not fixed)** the `02_BRANCHES/SFV_EVENTS.md` (CANON) contradiction — its DELIVERY section still reads "Pixieset or different? UNCONFIRMED" while Zenfolio is locked — with a [FOR HUMAN REVIEW] proposed one-line correction for Will to ratify before a follow-up session edits the CANON doc.
- Ends with an 8-row consolidated open-decisions / UNCONFIRMED table; CONNECTED FILES extended to the paper-trial + missing-files docs. Directive BLUEPRINT-LOOP-20260630-184711-P7-ZENFOLIO-CANON-001.

## 2026-06-30 — P6-UGC-DELIVERY: UGC client-delivery sub-system blueprinted (Claude Code)
- New doc `04_WORKFLOWS/UGC_DELIVERY.md` (STATUS: FOR HUMAN REVIEW) — focused expansion of the delivery half of the UGC money pipeline; covers coverage-map steps 15 (delivery), 16 (notification), 17 (client-memory write-back) and wires explicitly into `UGC_BUSINESS_PIPELINE.md` §5/§6/§9.
- Delivery platform presented as a FOR HUMAN REVIEW decision — **client portal vs Google Drive vs Pixieset** (Frame.io carried from the pipeline doc), with a revenue-branch trade-off table; no platform picked, no prices invented.
- Defines the end-to-end delivery path (approved master → stage → client-facing rename → upload → notify → revision → accept → memory write-back) and flags the MISSING notification step (channel/manual-vs-auto/template).
- CANON vs CANON-in-practice vs UNCONFIRMED vs MISSING labelled throughout; ends with an 8-row consolidated open-decisions table. Directive BLUEPRINT-LOOP-20260630-184410-P6-UGC-DELIVERY-001.

## 2026-06-30 — P4-IG-SCHEDULING: Instagram scheduling workflow blueprinted (Claude Code)
- New doc `04_WORKFLOWS/SCHEDULING_WORKFLOW.md` (STATUS: FOR HUMAN REVIEW) — closes MASTER GAP LIST P4 (IG scheduling, MISSING) for all 8 non-MYTHOLOGY branches.
- Covers: per-branch cadence/timing (all values UNCONFIRMED — none recorded in vault), caption insertion citing NAMING_CONVENTIONS caption system (CANON), carousel vs standalone handling, DELIVERY→scheduler hand-off, and a doc-only n8n integration point (live n8n untouched).
- Later vs Buffer left as a FOR HUMAN REVIEW decision with an unfilled criteria checklist — tool NOT picked; no prices/features invented.
- Ends with an 18-row consolidated open-decisions / UNCONFIRMED table. Directive BLUEPRINT-LOOP-20260630-184129-P4-IG-SCHEDULING-001.

## 2026-06-27 — BLOCK F: localFileTrigger fixed end-to-end (Claude Code)
- `03_INFRASTRUCTURE/n8n_env.ps1` (gitignored): added NODES_EXCLUDE=[], N8N_ENABLE_LOCAL_FILE_NODE=true; folded in NODE_FUNCTION_ALLOW_EXTERNAL=*, N8N_LOG_LEVEL=info; NODE_FUNCTION_ALLOW_BUILTIN → fs,path,os. Now single source of truth for n8n env.
- `03_INFRASTRUCTURE/start_n8n.ps1`: reduced to dot-source n8n_env.ps1 + `n8n start` (removed duplicate env defs).
- n8n workflows WF1 (vOH1CsPYvD27sUxx) + WF4 (nRbwsa0K62y2Fnmo): re-imported from canonical vault JSON to restore trigger→first-node connections stripped at original import; re-activated + published.
- Published all 3 active workflows (n8n 2.x publish model) — required for trigger registration.
- Deleted duplicate workflow `bf6LkL91FXDBF10F` (backed up first).
- Verified end-to-end: TEST-002 → OUTPUTS/TEST-002_RESULT.md (VALIDATED). Live process env confirmed, health 200.
- Flagged: WF4 Code node `process is not defined` bug; n8n API key not created (needs UI); Read Task BOM sensitivity. See SESSION_STATE 2026-06-27 block.

## 2026-05-29 — ULTRAPLAN — AI STACK GAP ANALYSIS COMPLETE

### New blueprint docs (20 gaps — all STATUS: FOR HUMAN REVIEW)
- `05_AI_LAYER/CONFIDENCE_LOGIC.md` — escalation bug diagnosis + fix spec + re-import checklist
- `03_INFRASTRUCTURE/POSTGRES_MIGRATION.md` — backup, install, migration, rollback
- `03_INFRASTRUCTURE/DOCKER_INSTALL_CHECKLIST.md` — install steps + what unlocks
- `03_INFRASTRUCTURE/FAILOVER_MODEL.md` — Ollama Node B fallback + n8n watchdog spec
- `03_INFRASTRUCTURE/SECRETS_POLICY.md` — key inventory, rotation plan, access control
- `05_AI_LAYER/ANTIGRAVITY_N8N_TRIGGER.md` — file-drop spec, job envelope rules, webhook future
- `03_INFRASTRUCTURE/N8N_MCP_SPEC.md` — czlonkowski/n8n-mcp Docker deploy, auth, workflow exposure
- `05_AI_LAYER/RESEARCH_ROUTE_SPEC.md` — Tavily vs Perplexity confirmed split; workflow3 FOR HUMAN REVIEW
- `05_AI_LAYER/GEMINI_INTEGRATION.md` — n8n→Gemini Flash API spec, env var, fallback
- `03_INFRASTRUCTURE/OPEN_WEBUI_SPEC.md` — Docker deploy, auth, n8n migration path
- `05_AI_LAYER/VECTOR_LAYER_PLAN.md` — Qdrant + nomic-embed-text, what gets embedded, RAG spec
- `04_WORKFLOWS/MEDIA_PIPELINE.md` — serial queue rules, FFmpeg, Whisper, faster-whisper path
- `03_INFRASTRUCTURE/MONITORING_STACK.md` — Prometheus + Grafana on Node B, alert thresholds
- `05_AI_LAYER/COST_CEILING_POLICY.md` — alert-only policy, COST_ALERTS.md log format
- `03_INFRASTRUCTURE/CONCURRENCY_QUEUE_SPEC.md` — PRIORITY enforcement, max-concurrent limits, Redis future
- `05_AI_LAYER/OUTPUT_VALIDATION.md` — per-task_type validation criteria, status tags
- `05_AI_LAYER/PROMPT_VERSIONING.md` — version naming, PROMPT_CHANGELOG.md, A/B testing
- `05_AI_LAYER/MODEL_LIFECYCLE_POLICY.md` — MODEL_LOCK.md, eval criteria, swap procedure
- `03_INFRASTRUCTURE/DISASTER_RECOVERY.md` — backup gaps, recovery runbooks, off-site plan

### Open question
- D3 (workflow3): not answered — flagged FOR HUMAN REVIEW in RESEARCH_ROUTE_SPEC.md

---

## 2026-05-24 — v0.1.0 — INITIAL BUILD SESSION

### Vault
- Full SFV_BLUEPRINT vault created via Python script
- All folders and files initialized with status tags
- Git initialized, first commit made
- Obsidian configured as blueprint brain

### Branches Defined
- MYTHOLOGY, SFV_LIVE, SFV_EVENTS, SFV_ATHLETICS, SFV_STUDIO
- SFV_UGC (name pending), SFV_ARCHIVE, SFV_WORLD, SFV_404
- Burner account: off Engine, not documented

### Infrastructure
- Storage architecture mapped (all drives assigned roles)
- Naming conventions locked
- Environment config with %SFV_ROOT% system
- Metadata system documented (UNCONFIRMED — Supabase schema TBD)

### AI Layer
- Model routing defined
- Ollama setup documented
- COST_ROUTING.md created
- Ollama daemon written and debugged (v2)
- TASK_QUEUE.md seeded with 3 audit tasks

### Tools
- TOOL_STATUS.md populated
- TOOLBOX.md created
- All tool decisions documented

### Optimization
- COMPRESSED_CONTEXT.md created (lean context for cheap model calls)
- SESSION_STATE.md created (session continuity)
- USAGE_OPTIMIZATION.md created (6 optimization strategies)
- CLAUDE.md optimized for Claude Code
- OLLAMA_PROMPTS.md created (full prompt library)

### Physical Setup
- Ollama installed on Engine (winget)
- qwen3 pulled (qwen3:14b pull initiated)
- Node.js installed
- Python confirmed working
- Git confirmed working
- Windows Terminal available
- Claude Code accessible via Code tab in Claude app

### Pending from this session
- Local GPT plugin: install + configure in Obsidian
- Smart Connections plugin: install in Obsidian
- qwen3:14b: confirm pull complete
- Ollama daemon: test run
- Wikilinks: add to branch files for graph view

## CONNECTED FILES
- [[MYTHOLOGY|Mythology Branch]]
- [[SFV_LIVE|SFV Live Branch]]
- [[STORAGE_ARCHITECTURE|Storage Architecture]]
- [[NAMING_CONVENTIONS|Naming Conventions]]
- [[MODEL_ROUTING|Model Routing]]
- [[OLLAMA_SETUP|Ollama Setup]]
- [[TOOL_STATUS|Tool Status]]
- [[COST_ROUTING|Cost Routing]]
