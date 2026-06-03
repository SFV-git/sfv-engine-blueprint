---
STATUS: ACTIVE
DATE: 2026-06-03
OWNER: WILL
PURPOSE: Autonomous overnight processing directive for SFV Engine
---

# OVERNIGHT DIRECTIVE — 2026-06-03

Read this at session start if waking from overnight. Report on completed tasks before doing anything else.

---

## WHAT IS RUNNING OVERNIGHT

| Service | Status | Notes |
|---|---|---|
| n8n | ACTIVE | workflow1 + workflow4 live. workflow2 pre-warm every 5 min. |
| Ollama | ACTIVE | qwen3:14b default. qwen2.5-coder:7b for CODE. minicpm-v:8b for VISION. |
| watchdog.ps1 | RUNNING | Checks n8n + Ollama every 5 min. Logs to WATCHDOG_LOG.md. Auto-restarts. |

---

## WHAT CLAUDE MAY DO AUTONOMOUSLY OVERNIGHT

1. **Process any HANDOFF files** in `99_INBOX/HANDOFFS/` — read, reason, write response to `99_INBOX/OUTPUTS/`
2. **Review FLAGGED outputs** in `99_INBOX/OUTPUTS/` — apply corrections, update status tag
3. **Append findings to DECISION_LOG.md** — one row per action, same format as existing rows
4. **Read vault docs** — any file in `C:\SFV_BLUEPRINT\` is readable

## WHAT CLAUDE MUST NOT DO OVERNIGHT

- Do NOT modify SESSION_STATE.md
- Do NOT promote any doc to CANON
- Do NOT delete any file
- Do NOT call external APIs (no Claude API, no Perplexity, no Tavily)
- Do NOT make creative decisions — escalate anything ambiguous back to HANDOFFS/
- Do NOT commit to git

---

## QUEUE STATUS AT DIRECTIVE WRITE TIME

Any PENDING tasks in `99_INBOX/QUEUE/` will be processed automatically by workflow1. Check DECISION_LOG.md for results.

---

## MORNING HANDOFF

At next session start:
1. Read WATCHDOG_LOG.md — any restarts overnight?
2. Read DECISION_LOG.md (last 20 rows) — what processed?
3. Read OUTPUTS/ (new files since overnight) — any FLAGGED?
4. Read HANDOFFS/ — anything Claude needs to resolve?
5. Report 3 lines. Wait for Will.

---

## CONNECTED FILES
- [[SESSION_STATE|Session State]]
- [[WATCHDOG_LOG|Watchdog Log]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[CONFIDENCE_LOGIC|Confidence Logic]]
