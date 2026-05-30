---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# MONITORING STACK — PROMETHEUS + GRAFANA + WINDOWS_EXPORTER

> Specifies the full Phase 3 monitoring deployment: windows_exporter on both nodes,
> Prometheus and Grafana on Node B, alert thresholds, and alert routing.
> Nothing in this document is deployed yet. This is the build spec.

---

## OVERVIEW

The monitoring stack provides visibility into Engine Body health and n8n/Ollama performance
without consuming Engine Body processing cycles. All collection, storage, and visualization
runs on Node B (R&D Terminal), which is designated 24/7.

This spec is Phase 3. Prerequisites: Docker, PostgreSQL, and Open WebUI must be stable
before this stack is deployed (per AI_STACK_ARCHITECTURE_BLUEPRINT §7 priority sequence).

---

## SECTION 1 — COMPONENT OVERVIEW

```
Node A (Engine Body)                Node B (R&D Terminal)
─────────────────────               ─────────────────────────────────────────
windows_exporter :9182   ──────→   Prometheus (Docker) — scrapes both nodes
                                         ↓
Node B (R&D Terminal)               Grafana (Docker) — reads Prometheus
windows_exporter :9182   ──────→     → Dashboard 14499 (Windows node overview)
                                     → Custom dashboards (n8n, Ollama, alerts)
                                         ↓
                                   Alert script (lightweight PS1)
                                     → Appends to 99_INBOX/FAILOVER_LOG.md
```

---

## SECTION 2 — WINDOWS_EXPORTER (BOTH NODES)

### Status

windows_exporter is already installed on both nodes (confirmed, per AI_STACK_ARCHITECTURE_BLUEPRINT).
No install action required. Verify it is running before Prometheus deployment.

### Verification Command (run on each node)

```powershell
# Confirm service is running
Get-Service -Name windows_exporter

# Confirm metrics endpoint is accessible
Invoke-WebRequest -Uri http://localhost:9182/metrics -UseBasicParsing | Select-Object StatusCode
```

Expected: `StatusCode 200`

### Port

Both nodes expose metrics on port **9182**.

Firewall rule required on both machines:
- Allow inbound TCP 9182 from `192.168.137.0/24` (direct ethernet subnet only)
- Node A firewall must allow Node B (192.168.137.239) to scrape 192.168.137.1:9182
- Node B firewall must allow itself to scrape localhost:9182 (already open)

[FOR HUMAN REVIEW]: Confirm windows_exporter firewall rule is in place on Node A.
AI_STACK_ARCHITECTURE_BLUEPRINT §1 lists port 9182 as needing to be open on the subnet,
but this has not been explicitly confirmed as done.

### Metrics Exposed

windows_exporter exposes the following metric categories by default:

| Collector | Metrics | Relevant For |
|-----------|---------|--------------|
| `cpu` | CPU utilization per core, idle/user/system % | Engine Body load during renders |
| `memory` | Available bytes, committed bytes, page faults | OOM risk with multiple models loaded |
| `logical_disk` | Read/write bytes/sec, % disk time, free space | D:\ throughput during ingest/export |
| `net` | Bytes sent/received per adapter | Direct ethernet link utilization |
| `service` | Service state (running/stopped) | n8n, Ollama, PostgreSQL health |
| `os` | System uptime, process count | General node health |
| `process` | Per-process CPU and memory | Ollama VRAM proxy (RAM-side) |

[INFERENCE]: GPU VRAM is not exposed natively by windows_exporter. Ollama VRAM usage must be
monitored via the Ollama API (`/api/ps`) or a separate GPU metrics exporter (e.g., DCGM or
a custom exporter). This is out of scope for Phase 3 base deployment.
[FOR HUMAN REVIEW]: Confirm whether GPU VRAM monitoring is required in Phase 3 or deferred.

---

## SECTION 3 — PROMETHEUS DEPLOYMENT ON NODE B

### Deployment Method

Docker container on Node B (R&D Terminal). Requires Docker installed on Node B.

[FOR HUMAN REVIEW]: Docker install on Node B is not confirmed in existing docs. Docker on
Node A is approved (2026-05-26, DOCKER_INSTALL_CHECKLIST.md). Node B Docker status is
[INFERENCE: likely required but not explicitly approved]. Confirm before Phase 3.

### Docker Run Command

```bash
docker run -d \
  --name prometheus \
  --restart unless-stopped \
  -p 9090:9090 \
  -v C:/sfv_monitoring/prometheus:/etc/prometheus \
  prom/prometheus \
  --config.file=/etc/prometheus/prometheus.yml
```

[INFERENCE]: Config volume path `C:/sfv_monitoring/prometheus` is proposed. Confirm Node B
storage location with Will before deploy.

### Prometheus Scrape Config

Create `prometheus.yml` at the config volume path:

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
      - targets: ['192.168.137.239:9182']
        labels:
          node: 'rd_terminal'
          role: 'sentinel'
```

Scrape interval of 15 seconds provides adequate granularity for detecting OOM events and
n8n queue backlog without excessive storage growth on Node B.

### Prometheus Access

Prometheus UI: `http://192.168.137.239:9090`
Available from Engine Body browser over direct ethernet.

---

## SECTION 4 — GRAFANA DEPLOYMENT ON NODE B

### Deployment Method

Docker container on Node B, same stack as Prometheus.

### Docker Run Command

```bash
docker run -d \
  --name grafana \
  --restart unless-stopped \
  -p 3001:3000 \
  -v C:/sfv_monitoring/grafana:/var/lib/grafana \
  grafana/grafana
```

Port mapping: internal 3000 → external **3001**.

[INFERENCE]: Port 3001 is chosen because port 3000 on Node A is allocated to Open WebUI
(per AI_STACK_ARCHITECTURE_BLUEPRINT Service Endpoint Registry). Node B does not run Open
WebUI, so 3000 may be available on Node B — but 3001 is used here as a safe default to
avoid future port conflicts if Open WebUI is ever deployed on Node B.
[FOR HUMAN REVIEW]: Confirm Grafana port. 3001 is the recommendation. Change if there is a
reason to use 3000 on Node B.

### Grafana Access

`http://192.168.137.239:3001`
Default credentials: admin / admin — change on first login.

### Dashboard Setup

**Base Dashboard:** Import Dashboard ID **14499** (Windows Node Overview for windows_exporter).
This provides immediate visibility into CPU, memory, disk, and network for both nodes.

**Custom Dashboards to Configure:**

| Dashboard | Key Panels | Data Source |
|-----------|-----------|-------------|
| n8n Queue Health | QUEUE folder file count over time, workflow execution rate | [INFERENCE: n8n does not natively expose Prometheus metrics — file count dashboard requires a custom exporter script or n8n API polling. Mark as Phase 3 stretch goal.] |
| Ollama Model Load | RAM usage of ollama.exe process, response latency trend | windows_exporter `process` collector + Ollama `/api/ps` custom exporter |
| Engine Body RAM | Available bytes, % committed, swap usage | windows_exporter `memory` collector |
| Disk Throughput | D:\ read/write MB/s during ingest/export windows | windows_exporter `logical_disk` collector |
| Node B Availability | Up/down status, last scrape time | Prometheus `up` metric |

[FOR HUMAN REVIEW]: n8n queue depth from Prometheus requires either a custom exporter that
counts files in QUEUE\ on a cron, or polling the n8n REST API. Confirm which approach is
preferred before building this panel.

---

## SECTION 5 — ALERT THRESHOLDS

All thresholds below are [INFERENCE] — they are reasonable defaults based on hardware specs.
Will must confirm values before alert rules are written into Prometheus or the alert script.

| Alert | Condition | Severity | Notes |
|-------|-----------|----------|-------|
| Engine Body GPU temp high | `gpu_temp_c > 85` | WARNING | [INFERENCE] Requires GPU exporter (not in windows_exporter default) |
| Engine Body RAM critical | `windows_memory_available_bytes / total < 0.15` (>85% used) | CRITICAL | 64GB node: fires at ~9.6GB free |
| n8n queue backlog | `queue_file_count > 10` for > 5 minutes | WARNING | [INFERENCE on count and duration] Requires custom file count exporter |
| Ollama response slow | `ollama_response_time_s > 60` | WARNING | [INFERENCE] Requires custom Ollama metrics exporter |
| Node B offline | Prometheus `up{job="rd_terminal"} == 0` for > 2 minutes | CRITICAL | Sentinel is down — monitoring blind |
| Engine Body offline | Prometheus `up{job="engine_body"} == 0` for > 2 minutes | CRITICAL | Primary node unreachable |
| Disk near full | `windows_logical_disk_free_bytes{volume="D:"} < 50GB` | WARNING | [INFERENCE on threshold] Adjust to actual D:\ capacity |

[FOR HUMAN REVIEW]: Confirm all threshold values. The RAM threshold of 85% and queue backlog
count of 10 are estimates. GPU temp monitoring requires a separate GPU exporter — confirm
whether this is in Phase 3 scope or deferred.

---

## SECTION 6 — ALERT ROUTING

### Phase 3 Scope: File-Based Alerts Only

No external notification (email, SMS, webhook) in Phase 3. Alerts write to a local log file.

A lightweight PowerShell script runs on Node B on a 60-second cron (or as a Windows
scheduled task) and queries the Prometheus API for active alerts.

### Alert Script Spec

Script location: `C:\SFV_BLUEPRINT\99_INBOX\prometheus_alert_writer.ps1` [INFERENCE on path]

Logic:

```powershell
# Query Prometheus alerts API
$alerts = Invoke-RestMethod -Uri "http://localhost:9090/api/v1/alerts" -Method GET

foreach ($alert in $alerts.data.alerts) {
    if ($alert.state -eq "firing") {
        $entry = "| $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | $($alert.labels.alertname) | $($alert.labels.severity) | $($alert.annotations.summary) |"
        Add-Content -Path "C:\SFV_BLUEPRINT\99_INBOX\FAILOVER_LOG.md" -Value $entry
    }
}
```

Output format matches the existing FAILOVER_LOG.md append-only table format
(established in FAILOVER_MODEL.md):

```
| 2026-05-29 14:32:01 | ENGINE_BODY_RAM_CRITICAL | CRITICAL | RAM usage at 87% — 8.3GB free |
| 2026-05-29 16:45:12 | N8N_QUEUE_BACKLOG | WARNING | 12 files in QUEUE for 7 minutes |
```

### Future Alert Routing (Post Phase 3)

[FOR HUMAN REVIEW]: The following options exist for external notifications when they are needed:
- n8n webhook trigger reading FAILOVER_LOG.md changes → POST to a notification endpoint
- Direct Grafana alerting via email SMTP (requires SMTP config)
- Grafana → Telegram or Slack webhook (requires channel setup)

No external notification is implemented in Phase 3. This is a future decision for Will.

---

## SECTION 7 — IMPLEMENTATION ORDER

Phase 3 is explicitly after Docker, PostgreSQL, and Open WebUI are stable on Node A.

| Step | Action | Node | Requires |
|------|--------|------|----------|
| 1 | Verify windows_exporter running on both nodes (`Get-Service`) | Both | windows_exporter already installed |
| 2 | Confirm port 9182 firewall rule allows 192.168.137.0/24 on Node A | Node A | Admin access |
| 3 | Install Docker on Node B | Node B | Will approval [FOR HUMAN REVIEW] |
| 4 | Create config directory `C:\sfv_monitoring\prometheus\` on Node B | Node B | Docker installed |
| 5 | Write `prometheus.yml` (Section 3 scrape config) | Node B | Config dir exists |
| 6 | Deploy Prometheus container | Node B | prometheus.yml written |
| 7 | Verify Prometheus scraping both nodes at `http://192.168.137.239:9090/targets` | Node B | Prometheus running |
| 8 | Deploy Grafana container | Node B | Prometheus running |
| 9 | Import Dashboard 14499 in Grafana | Node B | Grafana running |
| 10 | Configure Prometheus alert rules file | Node B | Thresholds confirmed by Will |
| 11 | Deploy alert writer PowerShell script as scheduled task on Node B | Node B | Alert rules confirmed |
| 12 | Verify FAILOVER_LOG.md receives test alert | Both | Alert script deployed |

---

## OPEN QUESTIONS FOR WILL

1. Is Docker approved for Node B? (It is confirmed for Node A but not explicitly for Node B.)
2. Confirm GPU temp monitoring scope — windows_exporter does not expose GPU temp natively.
3. Confirm all alert thresholds in Section 5 before alert rules are written.
4. Confirm Grafana port — 3001 is recommended; change if 3000 is preferred on Node B.
5. Confirm Whisper endpoint port on Node B (this doc references it in MEDIA_PIPELINE.md —
   listed as [INFERENCE] there as well).

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT]]
- [[RD_TERMINAL_ARCHITECTURE]]
- [[FAILOVER_MODEL]]
- [[DOCKER_INSTALL_CHECKLIST]]
- [[COST_CEILING_POLICY]]
