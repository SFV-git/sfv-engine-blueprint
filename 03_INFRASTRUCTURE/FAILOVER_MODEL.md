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
> Scenario 2 (n8n crash watchdog) is IMPLEMENTED — `03_INFRASTRUCTURE\watchdog.ps1`, running per OVERNIGHT_DIRECTIVE.
> Scenario 1 (Ollama Node B fallback) is spec-only — not yet built into workflow1.

---

## FAILURE SCENARIO 1 — Engine Body Ollama dies

**What breaks:** workflow1 HTTP Request node times out → all OLLAMA-routed tasks fail → queue backs up

**Current state:** No fallback. Tasks fail silently in n8n execution log.

**Failover target:** R&D Terminal Ollama at `http://192.168.137.246:11434`

### Spec: n8n fallback logic

In workflow1 "Call Ollama" node, add error handling:
```
Primary: POST http://127.0.0.1:11434/api/generate
On error/timeout:
  → retry once (2s delay)
  → if still failing: POST http://192.168.137.246:11434/api/generate
  → log fallback event to DECISION_LOG.md with tag FAILOVER_NODE_B
  → continue processing
```

**Conditions for this to work:**
- R&D Terminal must be online and Ollama running (it's designated 24/7)
- R&D Terminal needs qwen3:14b re-pulled — Ollama was wiped in the Win11 rebuild (2026-05-30) and is not yet reinstalled. This failover path is DEAD until the R&D Terminal install sequence completes.
- R&D Terminal does NOT need the same specialist models (qwen2.5-coder:7b, minicpm-v:8b) — fallback to qwen3:14b general model is acceptable for non-production tasks
- Network path: `192.168.137.246:11434` reachable from Engine Body (firewall /24 scope covers the new DHCP address)

**[FOR HUMAN REVIEW]:** Should fallback to Node B use the same specialist models or always fall back to qwen3:14b general? Recommend: qwen3:14b general — lower quality but avoids requiring specialist models on Node B.

---

## FAILURE SCENARIO 2 — n8n process crash

**What breaks:** All workflow triggers stop. QUEUE files pile up unprocessed. No notification.

**Current state:** IMPLEMENTED — `C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\watchdog.ps1` checks n8n (`/healthz`) and Ollama every 5 minutes, auto-restarts either if down, logs to `00_DEV_LOG\WATCHDOG_LOG.md`. Runs in a dedicated PowerShell window (not yet a Scheduled Task). n8n also auto-starts on login via `SFV_N8N.vbs`.

### Differences from original spec (actual implementation)

| Spec said | watchdog.ps1 does |
|---|---|
| 60-second interval | 300-second interval |
| Windows Scheduled Task | Manual PowerShell window — dies if window closed or on reboot until relaunched |
| Logs to 99_INBOX/FAILOVER_LOG.md | Logs to 00_DEV_LOG/WATCHDOG_LOG.md |
| n8n only | n8n + Ollama both |

**[FOR HUMAN REVIEW]:** (a) Promote watchdog to a Scheduled Task so it survives reboot/window close? (b) Keep WATCHDOG_LOG.md as its log, or redirect to FAILOVER_LOG.md per original spec? Recommend: Scheduled Task yes; keep WATCHDOG_LOG.md and reserve FAILOVER_LOG.md for Ollama-fallback and Prometheus events.

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
- [[WATCHDOG_LOG|Watchdog Log]]
- [[HARDWARE_CONTEXT|Hardware Context]]
- [[OVERNIGHT_DIRECTIVE|Overnight Directive]]
- [[DECISION_LOG|Decision Log]]
