---
STATUS: CANON
VERSION: v0.3.0
OWNER: WILL
LAST_UPDATED: 2026-05-26
---

# SESSION STATE

Read this first every session. Report in 3 lines. Wait for Will.

---

## STANDING ORDERS — DO NOT OVERRIDE WITHOUT WILL'S EXPLICIT INSTRUCTION
1. NO dev work until blueprint is fully planned and Will approves build order
2. NO deadlines drive decisions — long term correctness over short term delivery
3. Every feature must be planned to its full scaled form before any code is written
4. Plan what gets built, by which tool, in what order — FIRST. Always.
5. Physical node scaling must be accounted for in every architectural decision

## CURRENT PHASE
v0.x — Blueprint Lock (AI stack design + full blueprint planning. Zero dev work until complete.)

## PRIORITY ORDER (locked until Will says otherwise)
1. AI stack — design and link Claude + Antigravity + Ollama + n8n end to end. Token optimization. Full connection map.
2. Blueprint development — every workflow, every file, every decision documented before build begins.
   Includes: ingest (with culling), delivery, AI routing, physical node scaling, multi-computer architecture.
3. Build order — who builds what, when, in what sequence. Assigned per tool capability.
4. Dev work — only begins after 1-3 are complete and Will approves.

## LAST SESSION — 2026-05-25 (MAJOR SESSION)

### Stack built and operational:
- Full tool stack live: Claude Chat + Code + Cowork + Antigravity 2.0 + Ollama daemon + Obsidian + Google AI Studio + NotebookLM
- Drive paths locked: C:\=vault | D:\=Seagate One Touch 5TB | E:\=SanDisk Extreme 1TB
- Branch folders built on D:\ (49 folders, all 9 branches)
- Ollama daemon v3 running — fixed Windows path separator bug for READ: file injection
- vault_watcher.py v2 running — auto-adds CONNECTED FILES to new .md files
- find_orphans.py written — run to generate 00_DEV_LOG/ORPHANS.md

### Antigravity confirmed:
- Role: Agentic Orchestrator (PowerShell, web access, subagents, cron scheduling)
- Capabilities confirmed by Antigravity's own session
- ANTIGRAVITY.md context file written and live in vault root
- Git: SESSION_STATE.md + STACK_INTEGRATION_PLAN.md modified by Antigravity (not committed yet)
- ANTIGRAVITY_RULES.md shows as untracked in git — needs git add

### Blueprint docs built:
- 04_WORKFLOWS/INGEST.md — fully detailed, May 28 spec complete
- 99_INBOX/ingest.py v2 — all Gemini review issues fixed (config loader, correct duplicate behavior, lazy MD5, proper naming convention, dry-run without media)
- 05_AI_LAYER/RATE_LIMITS.md — all tools documented with limits + routing strategy
- 03_INFRASTRUCTURE/MULTI_AGENT_WORKFLOW.md — full tool interaction map
- 03_INFRASTRUCTURE/STACK_INTEGRATION_PLAN.md — updated by Antigravity
- 05_AI_LAYER/RD_TERMINAL_ARCHITECTURE.md — Sentinel proposal written (FOR HUMAN REVIEW)
- FOR_HUMAN_REVIEW/PROPOSALS.md — Proposal 007 (Sentinel) added by Antigravity

### Wikilinks:
- All 9 branch files: CONNECTED FILES sections added with cross-branch links
- All paths updated from %SFV_ROOT%\ACTIVE_STORAGE to %BRANCHES_ROOT%

### Corrections noted:
- Branch name is SFV_STUDIO not "SFV Studio" — all references should use underscore caps

## WHAT NEEDS ATTENTION NEXT SESSION
1. AI stack connection map — Claude + Antigravity + Ollama + n8n. Full design, token optimization, no code yet.
2. Ingest blueprint rewrite — culling during import, storage efficiency, full flow design including long term scaling.
3. Physical node architecture — Engine Body + R&D Terminal + future nodes. How they connect, what runs where.
4. Build order document — every file, every tool, every sequence. Will approves before anything gets coded.
5. n8n workflow JSONs have bad UUIDs — DO NOT import until blueprinted and rebuilt correctly.
6. Claude Code instance — currently paused, waiting. Do not resume until blueprint work is complete.
7. Docker install + restart — end of a future session when Will is ready.

## SESSION — 2026-05-26 (CONTINUED)
### Completed this session:
- AI_STACK_ARCHITECTURE_BLUEPRINT.md — STATUS: CANON, v1.1, 230 lines. AI stack priority item DONE.
- Full node linking, file allocation, phase sequence, all tools confirmed.
- Docker install initiated — requires restart to complete.

### FIRST TASK NEXT SESSION:
Build a lightweight terminal review system for all FOR HUMAN REVIEW and UNCONFIRMED items across the vault. No tokens — Will yes/no's them. Design + build at session start.
### Built (dev work — now paused pending blueprint completion):
- n8n_env.ps1 — API keys filled, Tavily live, Perplexity web-only
- .gitignore — n8n_env.ps1, .obsidian/, .smart-env/ excluded
- n8n_env.template.ps1 — safe placeholder for git
- ollama_queue_test.py — rewritten with Switch node routing + table log format
- workflow4_output_monitor.json — built but import failing (UUID issue)
- workflow1_queue_processor.json — built but import failing (UUID issue)
- QUESTIONS_FOR_WILL.md — 5 decisions resolved: UGC name, Later, Tailscale, Docker, Sentinel

### Decisions locked 2026-05-26:
- SFV_UGC stays as internal name
- Scheduling tool: Later
- Tailscale: approved
- Docker: approved (install end of session TBD)
- Proposal 007 Sentinel: approved
- Ingest routing: Option B fallback (C:\ if D:\ not present)
- NO MORE DEV WORK until blueprint is complete

## COMPLETED 2026-05-25 SESSION 2 — COMMUNICATION LAYER
- 00_DEV_LOG/2026-05-25_TODAY_CONTROL.md — created
- 05_AI_LAYER/AI_USE_CASE_PROFILE.md — created (Antigravity elevated to Tier 1, routing tree defined)
- 03_INFRASTRUCTURE/ENGINE_COMMUNICATION_MODEL.md — created (full comms model: queue, outputs, handoffs, decision log, routing rules)
- 99_INBOX/QUEUE/ — created. Perplexity task + Ollama test task queued.
- 99_INBOX/OUTPUTS/ — created
- 99_INBOX/HANDOFFS/ — created
- 99_INBOX/DECISION_LOG.md — created
- 99_INBOX/ollama_queue_test.py — created (reads JSON from QUEUE → Ollama → writes OUTPUTS → logs DECISION_LOG)
- 99_INBOX/OUTPUTS/20260525-002_INGEST_WASTE_AUDIT.md — ingest audited. No Claude waste. n8n trigger opps flagged FOR HUMAN REVIEW.

## OLLAMA QUEUE TEST — READY
  python C:\SFV_BLUEPRINT\99_INBOX\ollama_queue_test.py
  Test task: QUEUE/20260525-TEST-001_OLLAMA_BRANCH_CLASSIFY.json

## PERPLEXITY TASK — READY (run manually)
  Task prompt in: QUEUE/20260525-001_PERPLEXITY_N8N_INGEST_RESEARCH.json
  Save output to: OUTPUTS/20260525-001_PERPLEXITY_N8N_INGEST_RESEARCH.md

## CRITICAL DEADLINES
- MAY 28 THURSDAY — Morning Walk, 50+ models, SFV_STUDIO pipeline MUST work
- JUNE 6 — Shamar Tournament, SFV_LIVE pipeline
- THIS WEEK — Brandon Bellotti visit (first UGC client candidate)

## GIT STATUS (as of end of session 2026-05-25)
Files modified/untracked — NOT YET COMMITTED:
- M 03_INFRASTRUCTURE/STACK_INTEGRATION_PLAN.md
- M SESSION_STATE.md
- ?? 05_AI_LAYER/ANTIGRAVITY_RULES.md (untracked — needs git add)
- Multiple new files created tonight

Commit command:
  git add .
  git commit -m "feat: full stack operational — ingest v2, Sentinel proposal, wikilinks, daemon v3"

## OLLAMA DAEMON — HOW TO RUN
Ollama auto-starts. Do NOT run ollama serve (port conflict).
Run from Windows Terminal (PowerShell) — NOT inside Python interpreter.
Verify live: http://localhost:11434

  python C:\SFV_BLUEPRINT\99_INBOX\ollama_daemon.py

Results: C:\SFV_BLUEPRINT\99_INBOX\OLLAMA_RESULTS.md
Queue: C:\SFV_BLUEPRINT\99_INBOX\TASK_QUEUE.md (separate tasks with ---)

## VAULT WATCHER — HOW TO RUN
Run in dedicated terminal tab whenever doing vault work:
  python C:\SFV_BLUEPRINT\99_INBOX\vault_watcher.py
Auto-adds CONNECTED FILES to new .md files + queues Ollama for semantic links.

## LOCKED — DO NOT RE-DISCUSS
- 9 branches: MYTHOLOGY, SFV_LIVE, SFV_EVENTS, SFV_ATHLETICS, SFV_STUDIO, SFV_UGC, SFV_ARCHIVE, SFV_WORLD, SFV_404
- Branch name format: SFV_STUDIO (underscore + caps) — never "SFV Studio"
- Vault path: C:\SFV_BLUEPRINT
- Naming conventions: locked (see 03_INFRASTRUCTURE/NAMING_CONVENTIONS.md)
- Storage: C:\=vault | D:\=Seagate One Touch 5TB | E:\=SanDisk Extreme 1TB
- SFV_EVENTS delivery: Pixieset
- Model routing: Sonnet default, Opus on request, Gemini Flash for Antigravity
- Windows Terminal replaces Ghostty
- All paths via ENVIRONMENT_CONFIG.md — never hardcode

## HOW TO START NEXT SESSION
1. Claude reads SESSION_STATE.md + DASHBOARD.md + QUESTIONS_FOR_WILL.md
2. Claude reads OLLAMA_RESULTS.md for overnight output
3. Reports 3 lines max
4. Waits for Will
