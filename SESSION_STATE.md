---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# SESSION STATE

Read this first every session. Report in 3 lines. Wait for Will.

---

## CURRENT PHASE
v0.x — Blueprint Foundation (vault live, Ollama set up, moving to blueprint depth)

## LAST SESSION — 2026-05-25
- Antigravity added to stack (role UNCONFIRMED — Will to clarify)
- STACK_INTEGRATION_PLAN.md written to 03_INFRASTRUCTURE/
- Full model routing defined: Chat/Code/Cowork/Opus/Ollama/Antigravity
- Token optimization rules documented (7 rules)
- Two-version plan delivered: V1 (Chat+Obsidian+Ollama+Antigravity), V2 (+Code+Cowork)

## LAST SESSION — 2026-05-24
Everything built tonight:
- Full SFV planning session completed
- Vault built at C:\SFV_BLUEPRINT (Python script)
- Obsidian configured: Dataview, Templater, Obsidian Git, Metadata Menu, QuickAdd, Excalidraw, Smart Connections (install pending), Local GPT (install pending)
- Git initialized locally
- All 9 branches defined and documented
- All critical questions answered
- COMPRESSED_CONTEXT.md created
- COST_ROUTING.md created
- CLAUDE.md optimized for Claude Code
- USAGE_OPTIMIZATION.md created
- Ollama installed via winget
- qwen3 pulled (qwen3:14b pull may still be running)
- ollama_daemon.py written and debugged (v2)
- TASK_QUEUE.md seeded with 3 audit tasks
- OLLAMA_RESULTS.md created
- OLLAMA_SETUP.md created
- OLLAMA_PROMPTS.md created
- Claude Code accessible via Code tab in Claude desktop app
- Node.js installed
- Windows Terminal available (replaces Ghostty — no Windows support)

## WHAT NEEDS ATTENTION NEXT SESSION
1. Install remaining Obsidian plugins: Local GPT + Smart Connections
2. Configure Local GPT: Provider=Ollama, Model=qwen3:14b, URL=http://localhost:11434
3. Verify qwen3:14b finished pulling (ollama list in terminal)
4. Run ollama daemon and check OLLAMA_RESULTS.md for audit output
5. Deep blueprint work: 04_WORKFLOWS/INGEST.md (Thursday deadline)
6. 08_TESTS/PAPER_TRIAL_RUNS.md — Morning Walk walk-through before May 28
7. Scheduling tool decision (Later vs Buffer)
8. Add wikilinks to branch files for graph view

## CRITICAL DEADLINES
- MAY 28 THURSDAY — Morning Walk, 50+ models, Studio pipeline must work
- JUNE 6 — Shamar Tournament, Live pipeline
- THIS WEEK — Brandon Bellotti visit (first UGC client candidate)

## OLLAMA DAEMON — HOW TO RUN
Terminal Tab 1: ollama serve
Terminal Tab 2: python C:\SFV_BLUEPRINT\99_INBOX\ollama_daemon.py
Results land in: C:\SFV_BLUEPRINT\99_INBOX\OLLAMA_RESULTS.md
Add tasks to: C:\SFV_BLUEPRINT\99_INBOX\TASK_QUEUE.md separated by ---

## SETUP STEPS IF DAEMON FAILS
pip install requests
Then re-run daemon.

## LOCKED — DO NOT RE-DISCUSS
- 9 branches: MYTHOLOGY, LIVE, EVENTS, ATHLETICS, STUDIO, UGC, ARCHIVE, WORLD, 404
- Vault path: C:\SFV_BLUEPRINT
- Naming conventions: locked (see 03_INFRASTRUCTURE/NAMING_CONVENTIONS.md)
- Storage: 5TB Seagate=active, Internal NVMe=Engine intelligence
- SFV_EVENTS delivery: Pixieset
- abbass catch: auto + manual both
- Scheduling tool: TBD (open)
- Archive feed: both (promoted + dedicated shoots)
- Stories: Engine handles Studio + UGC only
- Cross-branch: FOR HUMAN REVIEW flag system
- Git: local, initialized
- All paths use %SFV_ROOT%
- Model routing: Sonnet default, Opus only on request
- Windows Terminal replaces Ghostty (Ghostty has no Windows version)
- Claude Code: accessed via Code tab in Claude desktop app (not separate install)

## HOW TO START NEXT SESSION
1. Claude reads this file
2. Claude reads DASHBOARD.md
3. Claude reads 00_DEV_LOG/QUESTIONS_FOR_WILL.md
4. Claude checks 99_INBOX/OLLAMA_RESULTS.md for overnight Ollama output
5. Reports 3 lines max
6. Waits for Will
