---
STATUS: CANON
VERSION: v0.2.0
OWNER: WILL
LAST_UPDATED: 2026-05-27
---

# FOR HUMAN REVIEW — PROPOSALS

Claude proposals awaiting Will's decision.
Nothing here gets built until Will explicitly approves.

---

## OPEN PROPOSALS

### PROPOSAL 008 — Vault Audit Fixes Applied (2026-06-09, Claude Chat) — RATIFIED 2026-06-25
Full-vault audit run (MYTHOS role, executed directly via Desktop Commander). Mechanical fixes applied — all factual corrections, no decisions made, no CANON status changed. Git diff shows every change. Ratify or revert per file:

**Stale IPs fixed (.239 → .246):** AI_STACK_ARCHITECTURE_BLUEPRINT (+ 192.168.10.0/24 typo → 137.0/24), FAILOVER_MODEL, MONITORING_STACK (scrape config), MEDIA_PIPELINE (4 refs)
**Stale claims corrected:** FAILOVER_MODEL (R&D qwen3:14b "confirmed" → needs re-pull; watchdog section rewritten to match the real watchdog.ps1), MONITORING_STACK (windows_exporter Node B → unverified post-Win11), LOCAL_MODELS (llama3.1 removed, env vars added, connection/electricity sections updated to approved state)
**Label/path fixes:** RATE_LIMITS (Ollama header → Engine Body primary), MODEL_LIFECYCLE_POLICY (MODEL_LOCK.md path)
**Refreshed:** COMPRESSED_CONTEXT v0.3.0 (32GB RAM, current tool/automation state, node IPs, Blueprint Lock + Antigravity≠approval rules), DASHBOARD (past deadlines closed, current work list), ENGINE_COMMUNICATION_MODEL (TASK_QUEUE.md marked LEGACY vs live n8n QUEUE\, Antigravity cost tier corrected to free Gemini Flash), UNCONFIRMED.md v0.2.0 (8 resolved items moved to resolved section)
**PROMPT_VERSIONING implemented:** handoff_generator_v1.txt + _CURRENT.txt + PROMPT_CHANGELOG.md created (CANON doc required them; original .txt untouched)
**Decision recorded:** Bitwarden as secrets manager → DISASTER_RECOVERY §3 + SECRETS_POLICY (action-pending flag kept until Will confirms entry)
**New doc:** 05_AI_LAYER/MYTHOS_PROTOCOL.md (FHR) — full-vault audit role, routing rule, dump command, cadence proposal

**NOT touched:** any CANON status, the 6 Antigravity-promoted docs (see QUESTIONS A1), backup_n8n.ps1 (dev work — see A2), OUTPUTS/ retention policy (needs a decision), workflow JSONs, SESSION_STATE history blocks.

---

## APPROVED PROPOSALS

### PROPOSAL 002 — Tailscale for Node Connection
Date: 2026-05-24 | Approved: 2026-05-26
Tailscale private network between Engine Body and R&D Terminal.
Remote access from school, location shoots.
→ APPROVED by Will 2026-05-26. Installed on both nodes.

---

### PROPOSAL 004 — R&D Terminal Idle Throttling
Date: 2026-05-24 | Approved: 2026-05-27
R&D Terminal idles by default. Will gives heads-up before a shoot.
Ollama idle mode active. ~40-60% power reduction when no active tasks.
n8n file watcher is negligible load — approved to run passively.
→ APPROVED by Will 2026-05-27.

---

### PROPOSAL 005 — SFV World as are.na Output Channel
Date: 2026-05-24 | Approved: 2026-05-27
Will-rejected content from SFV_WORLD → auto-queued to are.na pipeline folder.
Must be tagged/described so Will can decide final destination after the fact.
Manual upload to are.na for now. API integration later.
Will retains hard veto on any individual piece.
→ APPROVED by Will 2026-05-27.

---

### PROPOSAL 006 — Git Commit Convention
Date: 2026-05-24 | Approved: 2026-05-27
Commit format locked:
  feat: [new thing added]
  fix: [something corrected]
  docs: [blueprint updated]
  vault: auto-commit [timestamp]
  status: [file] moved from [old status] to [new status]
→ APPROVED by Will 2026-05-27.

---

### PROPOSAL 007 — Evolved R&D Terminal (Sentinel & Sandbox)
Date: 2026-05-25 | Approved: 2026-05-26
Full Sentinel architecture approved. Four roles: telemetry dashboard,
client review gateway, workflow optimization (Ollama), trading sandbox (Docker).
Details: 05_AI_LAYER/RD_TERMINAL_ARCHITECTURE.md
→ APPROVED by Will 2026-05-26.

---

## DEFERRED PROPOSALS

### PROPOSAL 001 — OpenClaw as R&D Terminal Agent
Date: 2026-05-24 | Deferred: 2026-05-27
Decided by: Claude (Will delegated)
OpenClaw deferred — no gap in current stack.
Ollama daemon + Antigravity already cover local batch + agentic orchestration.
If gaps appear post-v1.0, evaluate CrewAI or Open Interpreter as more mature alternatives.
→ DEFERRED — revisit post-v1.0.

---

### PROPOSAL 003 — UPS for Engine Protection
Date: 2026-05-24 | Deferred: 2026-05-27
APC Back-UPS 1500VA (~$150 CAD). Will confirmed eventual YES — not yet.
Purchase when full stack is running and lab setup is finalized.
→ DEFERRED — confirmed planned, timing TBD.

---

## REJECTED PROPOSALS
[Moved here once Will rejects — stays for record]

## CONNECTED FILES
- [[ENVIRONMENT_CONFIG|Environment Config]]
- [[OLLAMA_SETUP|Ollama Setup]]
- [[SFV_WORLD|SFV World]]
- [[RD_TERMINAL_ARCHITECTURE|RD Terminal Architecture]]
- [[NAMING_CONVENTIONS|Naming Conventions]]
- [[EXPORT|Export]]
