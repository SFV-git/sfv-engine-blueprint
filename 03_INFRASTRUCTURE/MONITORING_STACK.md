---
STATUS: FOR HUMAN REVIEW
VERSION: v0.2.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# MONITORING STACK — PROMETHEUS + GRAFANA + WINDOWS_EXPORTER

> Specifies the Phase 3 monitoring deployment.
> Decision 2026-05-29 (D-B): Prometheus and Grafana deploy on Node A (Engine Body), not Node B.
> Nothing in this document is deployed yet. This is the build spec.

---

## OVERVIEW

Prometheus and Grafana run as Docker containers on Node A alongside n8n and Open WebUI.
windows_exporter runs on both nodes, scraping is done by Prometheus on Node A.

**Trade-off from original spec:** Monitoring shares Engine Body resources instead of running on the dedicated Sentinel. Load is lightweight (Prometheus scrapes every 15s, Grafana serves dashboards on demand) — acceptable for Phase 3.

**Benefit:** No Docker approval needed for Node B. One fewer dependency to unblock.

---

## SECTION 1 — COMPONENT OVERVIEW

```
Node A (Engine Body)                         Node B (R&D Terminal)
──────────────────────────────────────────   ──────────────────────
windows_exporter :9182 ─────────────────→   windows_exporter :9182
                                                      │
Prometheus (Docker) :9090 ←─────────────────────────┘
  scrapes both nodes
      │
Grafana (Docker) :3001
  reads Prometheus
  Dashboard 14499 + custom dashboards
      │
Alert script (Windows Scheduled Task, Node A)
  queries Prometheus API
  → appends to 99_INBOX/FAILOVER_LOG.md
```

---

## SECTION 2 — WINDOWS_EXPORTER (BOTH NODES)

### Status

windows_exporter is installed on Node A (confirmed). Node B status is UNKNOWN post-Win11 rebuild (2026-05-30) — SESSION_STATE lists it as "not checked." Verify (and reinstall if missing) on Node B before Prometheus deployment.

### Verification (run on each node)

```powershell
Get-Service -Name windows_exporter
Invoke-WebRequest -Uri http://localhost:9182/metrics -UseBasicParsing | Select-Object StatusCode
```

Expected: `StatusCode 200`

### Firewall

- Node A must allow inbound TCP 9182 from `192.168.137.0/24` so Prometheus on Node A can scrape itself via the subnet IP
- Node B must allow inbound TCP 9182 from `192.168.137.1` (Node A Prometheus scraping Node B)

[FOR HUMAN REVIEW]: Confirm windows_exporter firewall rule is in place on both nodes. Port 9182 is listed in AI_STACK_ARCHITECTURE_BLUEPRINT §1 as needing to be open on the subnet, but has not been explicitly verified.

### Metrics Exposed

| Collector | Metrics | Relevant For |
|---|---|---|
| `cpu` | Utilization per core, idle/user/system % | Engine Body load during renders |
| `memory` | Available bytes, committed bytes, page faults | OOM risk with multiple models loaded |
| `logical_disk` | Read/write bytes/sec, % disk time, free space | D:\ throughput during ingest/export |
| `net` | Bytes sent/received per adapter | Direct ethernet link utilization |
| `service` | Service state (running/stopped) | n8n, Ollama, PostgreSQL health |
| `os` | System uptime, process count | General node health |
| `process` | Per-process CPU and memory | Ollama process RAM proxy |

[INFERENCE]: GPU VRAM is not exposed by windows_exporter natively. Ollama VRAM must be monitored via the Ollama API (`/api/ps`) or a separate GPU exporter. Out of scope for Phase 3 base deployment.

[FOR HUMAN REVIEW]: Is GPU VRAM monitoring required in Phase 3 or deferred?

---

## SECTION 3 — PROMETHEUS ON NODE A

### Deployment

```bash
docker run -d \
  --name prometheus \
  --restart unless-stopped \
  -p 9090:9090 \
  -v C:/sfv_monitoring/prometheus:/etc/prometheus \
  prom/prometheus \
  --config.file=/etc/prometheus/prometheus.yml
```

**Config volume:** `C:\sfv_monitoring\prometheus\` on Node A SSD.

### Scrape Config

Create `C:\sfv_monitoring\prometheus\prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'engine_body'
    static_configs:
      - targets: ['192.168.137.1:9182']
        labels:
          node: 'engine_body'
          role: 'primary'

  - job_name: 'rd_terminal'
    static_configs:
      - targets: ['192.168.137.246:9182']
        labels:
          node: 'rd_terminal'
          role: 'sentinel'
```

### Access

- From Node A: `http://localhost:9090`
- From Node B or Tailscale: `http://192.168.137.1:9090`

---

## SECTION 4 — GRAFANA ON NODE A

### Deployment

```bash
docker run -d \
  --name grafana \
  --restart unless-stopped \
  -p 3001:3000 \
  -v C:/sfv_monitoring/grafana:/var/lib/grafana \
  grafana/grafana
```

**Port:** 3001 — port 3000 is reserved for Open WebUI on Node A.

### Access

- From Node A: `http://localhost:3001`
- From Node B or Tailscale: `http://192.168.137.1:3001`
- Default credentials: admin / admin — change on first login

### Dashboard Setup

**Base:** Import Dashboard ID **14499** (Windows Node Overview for windows_exporter) — immediate visibility into CPU, memory, disk, network for both nodes.

**Custom dashboards to configure:**

| Dashboard | Key panels | Source |
|---|---|---|
| Engine Body RAM | Available bytes, % committed, swap | windows_exporter `memory` |
| Disk Throughput | D:\ read/write MB/s | windows_exporter `logical_disk` |
| Node B Availability | Up/down, last scrape time | Prometheus `up` metric |
| Ollama Model Load | RAM usage of ollama.exe, response latency | windows_exporter `process` + Ollama `/api/ps` |
| n8n Queue Health | QUEUE folder file count over time | [INFERENCE: requires custom exporter or n8n API polling — Phase 3 stretch goal] |

[FOR HUMAN REVIEW]: n8n queue depth requires either a custom file-count exporter or n8n API polling. Confirm which approach is preferred before building this panel.

---

## SECTION 5 — ALERT THRESHOLDS

All values are [INFERENCE] — reasonable defaults based on hardware specs. Will confirms before alert rules are written.

| Alert | Condition | Severity |
|---|---|---|
| Engine Body RAM critical | >85% RAM used (~9.6GB free on 64GB) | CRITICAL |
| Engine Body RAM warning | >75% RAM used | WARNING |
| Disk near full (D:\) | <50GB free | WARNING [INFERENCE on threshold] |
| n8n queue backlog | >10 PENDING files for >5 minutes | WARNING [INFERENCE — requires custom exporter] |
| Node B offline | `up{job="rd_terminal"} == 0` for >2 min | CRITICAL |
| Engine Body offline | `up{job="engine_body"} == 0` for >2 min | CRITICAL |
| Ollama response slow | Response time >60s | WARNING [INFERENCE — requires custom exporter] |

[FOR HUMAN REVIEW]: Confirm all threshold values before alert rules are built.
GPU temp monitoring is deferred pending a GPU exporter decision.

---

## SECTION 6 — ALERT ROUTING

Phase 3: file-based alerts only. No external notification (email, Slack, webhook).

A Windows Scheduled Task on Node A queries the Prometheus API every 60 seconds and appends firing alerts to `C:\SFV_BLUEPRINT\99_INBOX\FAILOVER_LOG.md`.

**Behavioral spec for alert writer script:**
- Input: Prometheus `/api/v1/alerts` endpoint at `http://localhost:9090`
- Trigger: every 60 seconds via Windows Task Scheduler
- For each firing alert: append one row to FAILOVER_LOG.md
- Row format matches FAILOVER_MODEL.md convention:

```
| 2026-05-29 14:32:01 | ENGINE_BODY_RAM_CRITICAL | CRITICAL | RAM at 87% — 8.3GB free |
| 2026-05-29 16:45:12 | N8N_QUEUE_BACKLOG | WARNING | 12 files in QUEUE for 7 min |
```

Script location (to be built during dev phase): `C:\SFV_BLUEPRINT\99_INBOX\prometheus_alert_writer.ps1`

**Future alert routing options (post Phase 3):**
- n8n webhook triggered by FAILOVER_LOG.md changes → external notification
- Grafana direct alerting via email SMTP
- Grafana → Telegram or Slack webhook

[FOR HUMAN REVIEW]: Confirm preferred external alert channel when Phase 3 is ready.

---

## SECTION 7 — IMPLEMENTATION ORDER

Prerequisites: Docker on Node A installed, PostgreSQL stable, Open WebUI stable.

| Step | Action | Node |
|---|---|---|
| 1 | Verify windows_exporter running on both nodes | Both |
| 2 | Confirm port 9182 firewall rule on Node A (allow 192.168.137.0/24 inbound) | Node A |
| 3 | Create config dir `C:\sfv_monitoring\prometheus\` on Node A | Node A |
| 4 | Write `prometheus.yml` (Section 3) | Node A |
| 5 | Deploy Prometheus container on Node A | Node A |
| 6 | Verify Prometheus scraping both nodes at `http://localhost:9090/targets` | Node A |
| 7 | Deploy Grafana container on Node A | Node A |
| 8 | Import Dashboard 14499 in Grafana | Node A |
| 9 | Confirm alert thresholds with Will | — |
| 10 | Write alert rules file (`alerts.yml`) for Prometheus | Node A |
| 11 | Deploy alert writer script as Windows Scheduled Task | Node A |
| 12 | Verify FAILOVER_LOG.md receives test alert entry | Node A |

---

## OPEN QUESTIONS FOR WILL

1. Confirm GPU temp monitoring scope — windows_exporter does not expose GPU temp natively.
2. Confirm all alert thresholds in Section 5 before rules are written.
3. Confirm Grafana port — 3001 is the default here; change if needed.
4. n8n queue depth panel approach — custom file-count exporter or n8n REST API polling?

---

## CONNECTED FILES
- [[FAILOVER_LOG|FAILOVER LOG]]
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture Blueprint]]
- [[TOOL_STATUS|Tool Status]]
- [[DASHBOARD|Dashboard]]
