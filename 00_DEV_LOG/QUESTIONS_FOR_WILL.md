---
STATUS: CANON
VERSION: v0.3.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
---

# QUESTIONS FOR WILL

---

## URGENT — FROM 2026-06-09 VAULT AUDIT

**A1. Antigravity CANON promotions — RESOLVED 2026-06-25.** ✅ Will ratified 5 of 6. DOCKER_INSTALL_CHECKLIST, SECRETS_POLICY, CONCURRENCY_QUEUE_SPEC, OUTPUT_VALIDATION, PROMPT_VERSIONING all confirmed CANON (were already promoted in 06-09 audit). N8N_MCP_SPEC held FHR until Docker + PostgreSQL live.

| Doc | Safe to ratify? | Notes |
|---|---|---|
| DOCKER_INSTALL_CHECKLIST | ✅ Yes | Clean. Correct prereq chains. No issues. |
| SECRETS_POLICY | ✅ Yes | Solid. Bitwarden decision now recorded. One open FHR (Tailscale port review) is correctly labeled. |
| CONCURRENCY_QUEUE_SPEC | ✅ Yes | Correctly sequences Phase 1 (no Redis) vs Phase 2 (Redis). SQLite warning aligns with CANON. Values labeled [INFERENCE] where appropriate. |
| OUTPUT_VALIDATION | ✅ Yes | Additive to QUALITY_CONTROL, not competing. Phase structure is sound. One open FHR (workflow5 standalone vs appended) is yours to decide. |
| PROMPT_VERSIONING | ✅ Yes | Implementation files now exist (created this session). CANON doc is fully satisfied. |
| N8N_MCP_SPEC | ⚠️ Conditional | Content is clean BUT has hard prereqs (Docker + PostgreSQL) that aren't CANON yet. Promoting it to CANON while its prereqs are FHR creates a dead spec. Recommend: ratify content, keep STATUS: FOR HUMAN REVIEW until Docker + PostgreSQL are confirmed live, then auto-promote. |

**Recommended action:** Ratify 5 of 6. Hold N8N_MCP_SPEC at FHR until Docker/PostgreSQL are done.

**A2. backup_n8n.ps1 — RESOLVED 2026-06-25.** ✅ Scheduled Task `SFV_n8n_Backup` registered (daily 03:00, RunLevel Highest). Verified Ready in Task Scheduler.

**A3. Bitwarden entry — PENDING (Will action required).** Keys not yet in Bitwarden. Will confirmed no. Do before going live with autonomous queue — without this, key rotation has no fallback.

**A4. Whisper port + endpoint on Node B.** Blocks the entire MEDIA pipeline build. Confirm port (9000? 8000?) and route when R&D Terminal is rebuilt.

**A5. Watchdog promotion — RESOLVED 2026-06-25.** ✅ Scheduled Task `SFV_Watchdog` registered (AtStartup, RunLevel Highest, restart 3x on failure). Verified Ready in Task Scheduler.

**A6. workflow IDs — RESOLVED 2026-06-25.** ✅ Verified via live n8n DB read. See SESSION_STATE 06-25 block. C4 closed.

---

## OPEN DECISIONS (from audit — answer when ready)

15. workflow5 validation: standalone workflow or appended node? (OUTPUT_VALIDATION)
16. pg_dump trigger: Task Scheduler (recommended — independent of n8n) or n8n cron? (DISASTER_RECOVERY §4)
17. Node B Ollama fallback: qwen3:14b only (recommended) or mirror specialists? (FAILOVER_MODEL)
18. MONITORING_STACK §5 alert thresholds + GPU VRAM scope + queue-depth approach — confirm before rules are written
19. Open WebUI: migrate workflow1 calls to it after Docker, or keep direct Ollama? (OPEN_WEBUI_SPEC)
20. Gemini API key: get from aistudio.google.com or defer GEMINI route?
21. MEDIA file types in scope: .mxf? .mkv? (MEDIA_PIPELINE §1)
22. DEFERRED MEDIA tasks: auto-retry after 5 min (recommended) or manual resubmit?
23. qwen3 think-mode policy: routing-config default with prompt override (recommended)? (PROMPT_VERSIONING)
24. Syncthing version history on Node B — enabled? (determines DR rollback Option B availability)
25. MYTHOS_PROTOCOL.md (new, FHR) — approve role + cadence?

---

## RESOLVED — 2026-06-03

~~workflow1 confidence escalation logic — 2/3 false escalations~~ → RESOLVED: fix validated end-to-end 2026-06-03. TEST_CLASSIFY_002 + TEST_CODE_004 both HIGH confidence → OUTPUTS/. CONFIDENCE_LOGIC.md promoted to CANON.

<details><summary>Original issue (archived)</summary>

Route tests 2026-05-29 results:
- VISION → minicpm-v:8b → COMPLETE ✅
- CLASSIFY → qwen3:14b → ESCALATED (should not have)
- CODE → qwen2.5-coder:7b → ESCALATED (should not have)

Cost routing breaks if Ollama always escalates. Claude Code diagnosis prompt was sent — read its findings first, then decide fix direction. DO NOT auto-patch.

</details>

---

## WHEN READY

10. WD EasyStore and WD Passport: audit when?

11. Porsche SSD file system fix: when?

12. Caption voice: define tone per branch when ready.

13. Video export specs: define resolution/format per branch.

~~14. qwen3:14b pull: confirm complete before running daemon.~~ → RESOLVED: confirmed in ollama list. 9.3 GB. Daemon clear to use it.

---

## RESOLVED (2026-05-27)

~~SFV_404 platform~~ → RESOLVED: own IG account confirmed.

~~Three monitors~~ → RESOLVED: 3 monitors on Engine Body, 2 on R&D Terminal. Current confirmed setup.

~~Whisper~~ → RESOLVED: local on R&D Terminal (free). No API cost.

---

## RESOLVED (2026-05-26)

~~SFV_UGC final name~~ → RESOLVED: stays SFV_UGC internally. IG handle may change over time, internal name does not.
~~Scheduling tool~~ → RESOLVED: Later. Better fit for visual/Instagram-heavy workflow with 8+ accounts.
~~Tailscale~~ → RESOLVED: approved. Will confirmed yes.
~~Docker~~ → RESOLVED: confirmed in stack. Install at end of tonight's session (requires restart — don't interrupt current work).
~~Proposal 007 (Sentinel)~~ → RESOLVED: approved. R&D Terminal architecture is a go.

## RESOLVED (2026-05-25)

~~Antigravity role~~ → RESOLVED: local vault executor. ANTIGRAVITY_RULES.md is CANON.
~~Obsidian plugins~~ → RESOLVED: all installed including Local GPT + Smart Connections.
~~Ollama serve error~~ → RESOLVED: error = Ollama already running. Skip `ollama serve`. Run daemon only.

---

## WHEN READY

~~WD EasyStore and WD Passport: audit when?~~ (still open)

~~Porsche SSD file system fix: when?~~ (still open)

~~Caption voice: define tone per branch when ready.~~ (still open)

~~Video export specs: define resolution/format per branch.~~ (still open)

~~qwen3:14b pull: confirm complete before running daemon.~~ (still open)

---
Last updated: 2026-05-27

## CONNECTED FILES
- [[DOCKER_INSTALL_CHECKLIST|Docker Install Checklist]]
- [[OUTPUT_VALIDATION|Output Validation]]
- [[DISASTER_RECOVERY|Disaster Recovery]]
- [[MONITORING_STACK|Monitoring Stack]]
- [[OPEN_WEBUI_SPEC|Open WebUI Specification]]
- [[SECRETS_POLICY|Secrets Policy]]
- [[CLAUDE|Claude]]
