---
STATUS: FOR HUMAN REVIEW
OWNER: WILL
CREATED_BY: Claude Code (Blueprint Builder, Opus) — 2026-06-27
PURPOSE: Handoff for the BLUEPRINT_AUDIT_CONTENT_BANK directive. STEP 1 done; STEP 2 barely started
  (cut short by session limit). This tells the next session exactly where to resume.
---

# HANDOFF — Blueprint Completeness Audit + Content Idea Bank

Directive: `00_DEV_LOG/DIRECTIVE_BLUEPRINT_AUDIT_CONTENT_BANK.md`

## WHAT GOT DONE THIS SESSION

**STEP 1 — COMPLETENESS AUDIT: COMPLETE. ✅**
- Ran 4 read-only audit subagents in parallel (Sonnet): A=production pipeline, B=UGC deep,
  C=R&D Terminal roles, D=infra+AI layer. No live system touched, no vault files modified by them.
- Merged all four into the STEP 1 deliverable: **`08_TESTS/BLUEPRINT_COVERAGE_MAP.md`** (FOR HUMAN REVIEW).
  It has: 4 domain coverage tables (step × node × software × doc × COVERED/THIN/MISSING), a scorecard,
  and an **18-item ranked MASTER GAP LIST (§6)** — the backlog STEP 2 works.

**Headline finding:** infra/AI layer is mostly *planned-but-THIN* (docs exist, execution pending). The real
**MISSING holes are in the creative/business craft layer**: no Premiere/video-edit doc, no IG scheduling
doc, no Lightroom preset/catalog doc, and the whole UGC money pipeline before/after the shoot
(lead → brief → contract → invoice → notify → report) is unblueprinted. The Content Idea Bank (Role 5)
does not exist in any form yet.

**STEP 2 — RESEARCH + FLESH OUT: NOT DONE (blocked by session limit).**
- Created task scaffold (TaskList #2–#6). Marked #1 (coverage map) complete.
- Launched 2 research subagents (E=ingestion/scraping services, F=storage/retrieval/scoring tech) with
  full prompts + WebSearch mandate + ICS/12GB constraints baked in. **Both returned 0 tokens — hit the
  Anthropic session limit (resets 8am America/Halifax).** No `TOOL_RESEARCH.md` content was produced.
  No `CONTENT_IDEA_BANK.md` written. No gap FHR docs written.

## RESUME HERE (exact next steps, in order)

1. **Re-run the two STEP 2 research subagents** (prompts are reusable — see directive §"Research mandate").
   - E — INGESTION: verify & cite Apify (+ MCP), Browse AI, social-scraping MCPs, are.na API, Reddit API
     tiers, RSS aggregation, trend APIs (Exploding Topics/Glimpse/pytrends), n8n community social nodes.
   - F — STORAGE/RETRIEVAL/SCORING: Qdrant vs Chroma vs **pgvector** (can it skip Qdrant since Postgres is
     already planned?), embedding model for small VRAM (nomic-embed-text / bge-small), 12GB-safe scoring
     model (qwen3:8b), flat-md vs SQLite vs Postgres vs vector-store trade-offs, retrieval MCP options, dedup.
   - Each writes a cited scratch file; then **append both into `10_REFERENCES/TOOL_RESEARCH.md`** with
     service / what-it-does / cost / ICS-compat / fit / verdict / source.
   - Scratch dir used this session: `…\scratchpad\` (RESEARCH_E_INGESTION.md / RESEARCH_F_STORAGE.md — empty/never written).
2. **Write `05_AI_LAYER/CONTENT_IDEA_BANK.md`** (FHR) — the P1 deliverable. 6 stages, each INPUT/PROCESS/
   OUTPUT + software + data-location: ingestion · processing (12GB-safe Ollama scoring) · storage · retrieval
   (how UGC_PRE_PRODUCTION pulls ideas) · feedback loop (QC outcomes re-score) · node boundary (R&D does
   24/7 work, Engine Body only pulls finished ideas). Respect ICS dependency + VRAM ceiling. Use the
   AUDIT_C scratch "ROLE 5 STUB" as the seed (it lists every connecting piece).
3. **Add Role 5 note to `RD_TERMINAL_ARCHITECTURE.md`** as an FHR edit (NOT a CANON rewrite).
4. **Work remaining ranked gaps** (one FHR doc each), per §6 of the coverage map. Likely next:
   P2 VIDEO_EDIT_WORKFLOW.md, P3 UGC business pipeline docs, P4 SCHEDULING_WORKFLOW.md.

## SCRATCH FILES FROM STEP 1 (still on disk this machine — source for the merged map)
`…\scratchpad\AUDIT_A_PRODUCTION.md`, `AUDIT_B_UGC.md`, `AUDIT_C_RDTERMINAL.md`, `AUDIT_D_INFRA.md`.
(The full directory is the session scratchpad; AUDIT_C has the richest Role 5 stub for the CONTENT_IDEA_BANK build.)

## GUARDRAILS HONORED (unchanged for next session)
- Blueprint Lock: everything written = FOR HUMAN REVIEW. No CANON promotion. No building. No live
  n8n/Ollama/Postgres changes. Will ratifies everything.
- No invention — STEP 2 research MUST verify + cite (it never ran, so nothing was invented).
- Do NOT bake the live Tavily key into any doc; key rotation is a prerequisite before new web-search wiring.
- Node isolation (Engine Body=worker, R&D Terminal=observer) + 12GB VRAM ceiling + ICS-internet dependency.

## FOR WILL
- Review `08_TESTS/BLUEPRINT_COVERAGE_MAP.md` — confirm the ranked gap order matches your priorities before
  STEP 2 spends effort writing docs in that sequence.
- Several P-items require *your decisions*, not just docs: UGC edit tool (Premiere vs CapCut vs Aditor.ai),
  scheduling tool (Later vs Buffer), CRM/contract/payment tools, UGC delivery platform. Flagged in §6.
- Pre-existing standing items still open: PROPOSAL 008, A1–A3 (Hermes), Tavily key rotation, n8n restart
  for WF4 fix. (Carried from prior handoffs — not touched this session.)

## CONNECTED FILES
- [[DIRECTIVE_BLUEPRINT_AUDIT_CONTENT_BANK|Directive]]
- [[BLUEPRINT_COVERAGE_MAP|Blueprint Coverage Map]]
- [[RD_TERMINAL_ARCHITECTURE|R&D Terminal Architecture]]
- [[CONTENT_BANKS|Content Banks]]
- [[RESEARCH_BANKS|Research Banks]]
- [[TOOL_RESEARCH|Tool Research]]
- [[SESSION_STATE|Session State]]
