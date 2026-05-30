---
STATUS: CANON
VERSION: v1.1
OWNER: WILL
LAST_UPDATED: 2026-05-26
---

# SFV Engine — AI Stack Architecture Blueprint

> **Node A (Engine Body):** Ryzen 9 9900X / RTX 5080 / 32GB — Primary production node
> *Note: RAM-dependent — confirm 64GB upgrade complete before deploying multiple large models simultaneously alongside Qdrant, PostgreSQL, and Redis.*
> **Node B (R&D Terminal):** RTX 3060 / 16GB — 24/7 Sentinel host

## Architecture Decision: Hub-and-Spoke 

The AI stack utilizes a strictly controlled hub-and-spoke pattern. At the core, **n8n** is the execution router, passing tasks between inference layers, storage paths, and logic processors. The system's overarching decision-maker and orchestrator is **Antigravity 2.0**.

The strict hierarchy is:
**Antigravity 2.0 → n8n → [Ollama | Open WebUI | Gemini Flash | Claude | Local Tools]**

- **Antigravity 2.0 (Tier 1):** Meta-controller. Spawns workflows, audits the codebase, schedules cron jobs, and issues top-level routing instructions.
- **n8n (Tier 2):** Deterministic workflow branching, trigger management, job queuing, and API connectivity.
- **Ollama / Open WebUI (Tier 3 - Inference First Pass):** First-pass classification, embeddings, and routing decisions (free, local, fast). Open WebUI acts as a unified OpenAI-compatible endpoint.
- **Gemini / Claude (Tier 4 - Inference Escalation):** Cloud burst execution and high-stakes complex reasoning.
- **Perplexity (Research Layer):** Web intelligence intake providing structured JSON/MD to the stack.

***

## Section 1: Full Connection Map

### Primary Data Flow (Node A)

```text
[Ingest Layer]
  File Drop / Watch Folder (n8n Local File Trigger watching %SFV_ROOT%\99_INBOX\QUEUE)
  Webhook (n8n POST endpoint)
  Perplexity → JSON queue file → %SFV_ROOT%\99_INBOX\QUEUE → n8n File Trigger

[Router Layer — n8n port 5678]
  ↓ HTTP Request node → Open WebUI / Ollama (port 11434) — classify/triage
  ↓ Switch node — route by job type
  ↓ Branch A: Local-only → Ollama (summarize, tag, classify, embed)
  ↓ Branch B: Cloud burst → Gemini Flash API (bulk transform, reformat)
  ↓ Branch C: High-stakes → Claude API (blueprint, architecture, final copy)
  ↓ Branch D: Media → FFmpeg (via Execute Command node) → Whisper HTTP
  ↓ Branch E: Research → NotebookLM (manual) / Perplexity (API/queue drop)

[Output Layer]
  → Obsidian vault (file write via n8n to %SFV_ROOT%\99_INBOX\OUTPUTS\)
  → Supabase (future: HTTP Request → REST API or Postgres node)
  → Antigravity artifact store (structured JSON/MD files)
```

### Node Linking & Networking Configuration

**1. Direct Ethernet Configuration (ICS — confirmed 2026-05-27)**
Engine Body shares WiFi internet to R&D Terminal via Windows ICS over direct ethernet cable.
- **Node A (Engine Body):** `192.168.137.1` (ICS host — assigned automatically by Windows)
- **Node B (R&D Terminal):** `192.168.137.239` (ICS client — DHCP assigned)
- **Node A Tailscale:** `100.118.181.52`
- **Node A home WiFi:** `192.168.2.12`
Windows Defender Firewall on both machines must allow inbound SMB (445) and application ports (11434, 5678, 9090, 9182) from the `192.168.137.0/24` subnet.
NOTE: R&D Terminal has no WiFi card. Internet provided via ICS through ethernet. Long-term: add USB WiFi adapter to restore clean architecture.

**2. Tailscale Coexistence Rule (CRITICAL)**
Tailscale is exclusively for remote access (`100.x.x.x`). Do not advertise `192.168.10.0/24` as a Tailscale subnet route, as Windows gVisor Netstack routing will degrade direct-link throughput. Isolation to the direct IP is mandatory for inter-node production traffic.

**3. Cross-Node File Access (SMB)**
Node A shares the vault as `VaultShare`; Node B maps a network drive to `\\192.168.137.1\VaultShare`. This provides native Windows performance for active edits.

**4. Ollama Cross-Node Inference**
Set `OLLAMA_HOST=0.0.0.0:11434` as a system environment variable on Node A. Node B directs heavy inference calls to `http://192.168.137.1:11434/api/generate`.

### Service Endpoint Registry

| Service | Host | Port | Protocol | Data Direction | Phase |
|---|---|---|---|---|---|
| n8n | Node A | 5678 | HTTP (localhost) | Bi-directional router | Active |
| PostgreSQL | Node A | 5432 | TCP (localhost) | n8n DB Backend | Immediate |
| Open WebUI | Node A | 3000 | HTTP REST | Unified Inference API | Phase 1 |
| n8n-MCP | Node A | stdio | MCP | Claude/Antigravity → n8n | Phase 1 |
| Ollama (Node A) | Node A | 11434 | HTTP REST | Primary | Active |
| Ollama (Node B) | Node B | 11434 | HTTP REST | Sentinel fallback | Active |
| windows_exporter | Nodes A+B| 9182 | HTTP | Metrics → Prometheus | Phase 1 |
| Qdrant [FUTURE] | Node A | 6333 | HTTP REST | n8n / Python → Node A | Phase 2 |

***

## Section 2: Storage & Sync Strategy

### File Allocation Strategy

| Component | Node | Drive | Rationale |
|-----------|------|-------|-----------|
| Obsidian Vault | A | `C:\` | SSD speed for frequent reads/writes |
| Ollama models | A | `D:\` | Large models don't need SSD; hot path is GPU VRAM |
| n8n data & Postgres DB | A | `C:\` | DB read/write performance is critical for webhook speed |
| Raw media ingest | A | `D:\` | Bulk storage capacity |
| Queue / handoff files | A | `C:\` | Fast IO for n8n trigger responsiveness |
| Qdrant vector DB | A | `C:\` | Vector search latency demands SSD |

### Sync Strategy
- **Vault Sync:** Syncthing (OSS) running as a Windows service handles real-time bidirectional sync over the direct ethernet link between Node A and Node B. Replaces paid Obsidian Sync.
- **Media Backup:** Scheduled Robocopy task nightly from Node A (`D:\`) to Node B.

***

## Section 3: Token/Cost Routing Strategy

The routing decision occurs at the classifier level before any expensive API calls are executed.

### Routing Decision Tree

```text
INBOUND TASK
  ↓
[Ollama / Open WebUI] — qwen3:14b via n8n HTTP Request node
  Output: { tier: "local" | "cloud_cheap" | "cloud_premium", job_type: string }
  ↓
TIER: local (Free)
  → qwen3:14b (General text, metadata)
  → qwen3.6-coder / DeepSeek Coder V2 Lite (Code, Python ingest authoring)
  → minicpm-v (Vision, thumbnails, OCR)
  → Use for: tagging, classification, summarization <2000 tokens, embeddings

TIER: cloud_cheap (Free/Low-Cost Burst)
  → Gemini Flash
  → Use for: bulk reformatting, caption generation at scale, Antigravity orchestration ops

TIER: cloud_premium (High Cost)
  → Claude Sonnet (default) / Opus (escalation only)
  → Use for: architecture documents, final deliverables, deep system judgment
```

### Cost Guard Rules and Escalation Conditions

1. **Classification is always free:** Use Ollama for all routing decisions.
2. **Flash free tier limits:** If Gemini Flash hits request limits, fall back to Ollama.
3. **Escalation Trigger:** A task is only escalated to Claude if Ollama's response contains explicit doubt language, or if the job envelope includes `"client_facing": true`. The authoritative keyword list and escalation logic is in `05_AI_LAYER/CONFIDENCE_LOGIC.md`. Numeric threshold (< 0.75) is retired — keyword matching is the live implementation as of commit 8c7188f.
4. **Code and Vision Routing:** Explicitly route code and vision tasks to the dedicated specialist models (Coder/minicpm-v) on Node A, not the general qwen model.

***

## Section 4: n8n Triggers, Schemas, & Execution Optimizations

### Trigger Inventory

| Trigger Type | n8n Node | Use Case |
|---|---|---|
| File system watch | Local File Trigger | Perplexity queue files in `%SFV_ROOT%\99_INBOX\QUEUE` |
| Scheduled cron | Schedule Trigger | Daily Sentinel health report, 5-min Ollama pre-warm |
| HTTP webhook | Webhook | Antigravity task dispatch, cross-node alerts |
| Manual | Manual Trigger | Testing, development runs |

### Standard Job Envelope Schema

See `05_AI_LAYER/JOB_ENVELOPE_SPEC.md` for the full canonical schema including all optional fields and task_type extensions. Base fields:

```json
{
  "task_id": "YYYYMMDD-###",
  "task_type": "CLASSIFY | SUMMARIZE | COMPRESS | RESEARCH | BLUEPRINT | CODE | MEDIA | VISION | GEMINI",
  "topic": "String",
  "prompt": "String",
  "priority": "NORMAL | HIGH | CRITICAL",
  "status": "PENDING | IN_PROGRESS | COMPLETE | ESCALATED | DEFERRED | BLOCKED | DRAFT",
  "output_target": "%SFV_ROOT%\\99_INBOX\\OUTPUTS\\[filename]"
}
```

### Critical Execution Optimizations

- **Ollama Cold Start Prevention:** Set `OLLAMA_KEEP_ALIVE=10m` and run a cron workflow every 5 minutes to ping the primary models to keep them in VRAM.
- **SQLite Locking:** SQLite corrupts under parallel webhook hits. **PostgreSQL migration is mandatory** before concurrent execution scaling.

***

## Section 5: Sentinel Role (Node B)

The **Sentinel** resides on Node B (R&D Terminal - RTX 3060) for 24/7 observation and Engine Body health monitoring.

**Monitoring Stack:**
- **windows_exporter:** Deployed on both nodes to expose CPU, memory, disk, and service states as Prometheus metrics.
- **Prometheus + Grafana:** Deployed on Node B to scrape metrics (Dashboard ID: 14499) and observe n8n queue depth and queue failures.

***

## Section 6: Gaps and Mitigations

The following critical Single Points of Failure (SPOFs) and gaps exist and are actively mitigated:

| Component | Failure Mode | Impact | Mitigation |
|---|---|---|---|
| n8n SQLite DB | Database lock / corruption | **Critical** | Migrate to PostgreSQL (Immediate priority). |
| n8n process crash | All routing stops | **Critical** | Queue mode (Redis) [FUTURE] + PostgreSQL prevents UI blocking. |
| Node B offline | Ollama unavailable | **High** | Node A Ollama acts as hot fallback. |
| Concurrent Whisper | OOM memory crash | **High** | Serial media queue; deploy `faster-whisper` [FUTURE]. |
| RAM limits (32GB) | System swap crash | **High** | Enforce model unloading discipline; monitor via Grafana. |

***

## Section 7: Prioritized Action Sequence

| Priority | Action | Phase |
|----------|--------|-------|
| 🔴 Critical | Migrate n8n to PostgreSQL (before any queue mode work) | Immediate |
| 🔴 Critical | Add `windows_exporter` to both nodes | Immediate |
| 🔴 Critical | Set static IPs on direct ethernet NICs; enforce Tailscale isolation | Immediate |
| 🟠 High | Set `OLLAMA_HOST=0.0.0.0:11434` on Node A; firewall-restrict | Phase 1 |
| 🟠 High | Deploy n8n-MCP (czlonkowski/n8n-mcp) via Docker | Phase 1 |
| 🟠 High | Deploy Open WebUI on Node A | Phase 1 |
| 🟠 High | Add qwen3.6-coder / DeepSeek Coder V2 Lite to Node A | Phase 1 |
| 🟠 High | Set `OLLAMA_KEEP_ALIVE=10m`; add pre-warm cron | Phase 1 |
| 🟡 Medium | Add minicpm-v (verify Ollama version compatibility first) | Phase 2 |
| 🟡 Medium | Deploy Qdrant + nomic-embed-text; begin embedding vault | Phase 2 |
| 🟡 Medium | Deploy Redis + switch n8n to queue mode | Phase 2 |
| 🟡 Medium | Set up Syncthing for vault sync Node A → Node B | Phase 2 |
| 🟢 Low | Configure Prometheus to scrape both windows_exporter instances | Phase 3 |

***

## Section 8: Recommended Add-Ons [FUTURE]

> **STATUS:** [FUTURE]
> These add-ons are approved, but remain labeled [FUTURE] until installed.

1. **Redis [FUTURE]:** Job queue broker for n8n. Separates editor process from execution workers.
2. **Qdrant [FUTURE]:** Rust-based vector memory layer running locally on Node A.
3. **`nomic-embed-text` [FUTURE]:** Local embedding model running via Ollama.
4. **`faster-whisper` [FUTURE]:** Python Flask backend replacing standard OpenAI Whisper.
5. **Prometheus + Grafana [FUTURE]:** Sentinel monitoring stack deployed on Node B.

***

> **FOR HUMAN REVIEW:**
> - minicpm-v Ollama version check — APPROVED 2026-05-26. Run `ollama --version` before Phase 2 deploy to confirm compatibility.

## CONNECTED FILES
- [[ANTIGRAVITY|Antigravity 2.0]]
- [[N8N_BLUEPRINT|n8n Workflow Blueprint]]
- [[CLAUDE_API|Claude API Integration]]
- [[OLLAMA_SETUP|Ollama Local Inference Setup]]
- [[ENVIRONMENT_CONFIG|Environment Networking Configuration]]
