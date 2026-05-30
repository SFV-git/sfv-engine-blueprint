---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# FAILOVER MODEL — OLLAMA + n8n RESILIENCE

> Documents what happens when primary services go down and how recovery is triggered.
> No automatic recovery is implemented yet — this is the spec for what to build.

---

## FAILURE SCENARIO 1 — Engine Body Ollama dies

**What breaks:** workflow1 HTTP Request node times out → all OLLAMA-routed tasks fail → queue backs up

**Current state:** No fallback. Tasks fail silently in n8n execution log.

**Failover target:** R&D Terminal Ollama at `http://192.168.137.239:11434`

### Spec: n8n fallback logic

In workflow1 "Call Ollama" node, add error handling:
```
Primary: POST http://127.0.0.1:11434/api/generate
On error/timeout:
  → retry once (2s delay)
  → if still failing: POST http://192.168.137.239:11434/api/generate
  → log fallback event to DECISION_LOG.md with tag FAILOVER_NODE_B
  → continue processing
```

**Conditions for this to work:**
- R&D Terminal must be online and Ollama running (it's designated 24/7)
- R&D Terminal has qwen3:14b pulled (confirmed)
- R&D Terminal does NOT need the same specialist models (qwen2.5-coder:7b, minicpm-v:8b) — fallback to qwen3:14b general model is acceptable for non-production tasks
- Network path: `192.168.137.239:11434` reachable from Engine Body (confirmed — firewall rules set)

**[FOR HUMAN REVIEW]:** Should fallback to Node B use the same specialist models or always fall back to qwen3:14b general? Recommend: qwen3:14b general — lower quality but avoids requiring specialist models on Node B.

---

## FAILURE SCENARIO 2 — n8n process crash

**What breaks:** All workflow triggers stop. QUEUE files pile up unprocessed. No notification.

**Current state:** n8n auto-starts on login via `SFV_N8N.vbs` launcher, but does not restart on crash mid-session.

### Spec: Watchdog process

A lightweight PowerShell watchdog script checks n8n health every 60 seconds:

**Behavioral spec for watchdog:**
- Runs every 60 seconds as a Windows Scheduled Task on Node A
- Health check: HTTP GET to `http://127.0.0.1:5678/healthz` — expects 200 OK
- On failure: wait 10 seconds, retry once
- On second failure: relaunch n8n using the same startup command as `SFV_N8N.vbs`
- On relaunch: append one row to `C:\SFV_BLUEPRINT\99_INBOX\FAILOVER_LOG.md`
- Row format: `| [timestamp] | N8N_CRASH | Watchdog restarted n8n | — | [task count] tasks requeued |`
- Script to build during dev phase: `C:\SFV_BLUEPRINT\99_INBOX\n8n_watchdog.ps1`

**[INFERENCE]:** n8n exposes `/healthz` endpoint at the same port. Confirm this is accessible before implementing.

---

## FAILURE SCENARIO 3 — Engine Body offline / reboot

**What breaks:** n8n stops, queue stops, vault watcher stops.

**Current state:** Both n8n and vault_watcher auto-start on login. Recovery = login.

**No additional spec needed.** Auto-start handles this. Queue files persist on disk — n8n picks them up on restart via file trigger.

**Caveat:** SQLite DB may corrupt if Engine Body loses power mid-write. PostgreSQL migration (Gap 2) eliminates this risk.

---

## FAILURE SCENARIO 4 — R&D Terminal offline

**What breaks:** Sentinel monitoring loses visibility. Node B Ollama unavailable (but Node A is primary — this is the fallback, not the primary).

**Current state:** Acceptable degradation. Engine Body continues without Sentinel telemetry. Monitoring stack (Prometheus/Grafana) is FUTURE.

**No blocking action required.** R&D Terminal is observer/fallback only — its failure does not stop production.

---

## FAILOVER LOG FORMAT

`99_INBOX/FAILOVER_LOG.md` — append-only:

```
| 2026-05-29 14:32:01 | OLLAMA_TIMEOUT | Switched to Node B | qwen3:14b | 3 tasks rerouted |
| 2026-05-29 16:45:12 | N8N_CRASH | Watchdog restarted n8n | — | 2 tasks requeued |
```

---

## IMPLEMENTATION ORDER

| Priority | Action | Requires |
|---|---|---|
| 🔴 Now | PostgreSQL migration — eliminates SQLite crash risk | Will's time |
| 🟠 Phase 1 | n8n Node B fallback in workflow1 | workflow1 re-import |
| 🟠 Phase 1 | n8n_watchdog.ps1 + Startup registration | Script build |
| 🟡 Phase 2 | Alert on failover event (webhook or file) | COST_CEILING_POLICY |
| 🟢 Phase 3 | Prometheus alert rules for Ollama/n8n health | MONITORING_STACK |

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture §6]]
- [[POSTGRES_MIGRATION|PostgreSQL Migration]]
- [[MONITORING_STACK|Monitoring Stack]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[RD_TERMINAL_ARCHITECTURE|R&D Terminal Architecture]]
