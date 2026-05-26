---
STATUS: CANON
VERSION: v1.0
OWNER: WILL
LAST_UPDATED: 2026-05-26
---

# SFV Engine — AI Stack Architecture Blueprint

> **Node A (Engine Body):** Ryzen 9 9900X / RTX 5080 / 32GB — Primary production node
> **Node B (R&D Terminal):** RTX 3060 / 16GB — 24/7 Sentinel host

## Architecture Decision: Hub-and-Spoke 

The AI stack utilizes a strictly controlled hub-and-spoke pattern. At the core, **n8n** is the execution router, passing tasks between inference layers, storage paths, and logic processors. However, the system's overarching decision-maker and orchestrator is **Antigravity 2.0**.

The strict hierarchy is:
**Antigravity 2.0 → n8n → [Ollama | Gemini Flash | Claude | Local Tools]**

- **Antigravity 2.0 (Tier 1):** Meta-controller. Spawns workflows, audits the codebase, schedules cron jobs, and issues top-level routing instructions.
- **n8n (Tier 2):** Deterministic workflow branching, trigger management, job queuing, and API connectivity.
- **Ollama/qwen3:14b (Tier 3 - Inference First Pass):** First-pass classification, embeddings, and routing decisions (free, local, fast).
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
  ↓ HTTP Request node → Ollama (port 11434) — classify/triage
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

### Cross-Node Communication (Node A ↔ Node B)

```text
Node B (Sentinel / RTX 3060)
  Ollama qwen3:14b — 24/7 local inference (port 11434)
  Health monitor — polls Node A services every 60s
  Sentinel workflow (Python watchdog / Prometheus + Grafana [FUTURE])

Communication methods:
  Node A → Node B: HTTP POST to Node B's Ollama API (direct inference)
  Node B → Node A: HTTP POST to Node A's n8n webhook (alert/report)
  Shared: Network folder mount or structured HTTP file exchange
```

**Ollama Distribution — UNCONFIRMED [FOR HUMAN REVIEW]**
Which node runs Ollama as primary depends on two unresolved factors:
1. **Ollama's role at runtime** — if Ollama is purely a cheap inference layer (classify, tag, embed), Node B (24/7, always-on) is the natural primary. If Ollama is also used for heavy local generation during active sessions, Node A (RTX 5080) is faster.
2. **Tailscale connection quality** — if Node A → Node B latency over Tailscale is acceptable for inline inference calls, Node B primary works. If latency is too high for synchronous routing decisions, Node A must be primary.

Decision rules (to be confirmed by Will after Tailscale is live):
- Node B primary if: Ollama role = classification/embedding only AND Tailscale latency < 20ms
- Node A primary if: Ollama used for generation during active sessions OR Tailscale not yet live
- Both nodes run Ollama regardless — the primary/fallback assignment is a routing config in n8n only

### Service Endpoint Registry

| Service | Host | Port | Protocol | Data Direction |
|---|---|---|---|---|
| n8n | Node A | 5678 | HTTP (localhost) | Bi-directional router |
| Ollama (Node A) | Node A | 11434 | HTTP REST | Local fallback or primary (TBD) |
| Ollama (Node B) | Node B | 11434 | HTTP REST | 24/7 inference or primary (TBD) |
| Qdrant [FUTURE] | Node A | 6333 | HTTP REST | n8n / Python → Node A |
| Supabase | Cloud | 443 | HTTPS REST | n8n → Cloud |
| Claude API | Cloud | 443 | HTTPS REST | n8n / Antigravity → Cloud |
| Gemini Flash API | Cloud | 443 | HTTPS REST | n8n / Antigravity → Cloud |

***

## Section 2: Token/Cost Routing Strategy

The routing decision occurs at the classifier level before any expensive API calls are executed. The cheapest capable layer receives the task.

### Routing Decision Tree

```text
INBOUND TASK
  ↓
[Ollama Classifier] — qwen3:14b via n8n HTTP Request node
  Output: { tier: "local" | "cloud_cheap" | "cloud_premium", job_type: string }
  ↓
TIER: local (Free)
  → Ollama qwen3:14b (Node B preferred, Node A fallback)
  → Use for: tagging, classification, summarization <2000 tokens, embeddings, metadata extraction, routing decisions, draft generation, Obsidian note formatting

TIER: cloud_cheap (Free/Low-Cost Burst)
  → Gemini Flash
  → Use for: bulk reformatting, caption generation at scale, high-volume transcription cleanup, content structuring, Antigravity orchestration operations, anything requiring >2000 token context without high architectural quality bar

TIER: cloud_premium (High Cost)
  → Claude Sonnet (default) / Opus (escalation only)
  → Use for: architecture documents, final deliverables, blueprint generation, client-facing copy, any task requiring deep system judgment + precision
```

### Cost Guard Rules and Escalation Conditions

1. **Classification is always free:** Never call Claude for classification. Use Ollama for all routing decisions.
2. **Flash free tier limits:** If Gemini Flash hits request limits, fall back to Ollama, not Claude.
3. **Claude Opus is emergency-only:** Sonnet handles 95% of premium tasks. Opus is explicitly requested by Will for multi-turn complex architecture sessions only.
4. **Token budget check:** Jobs must be pre-estimated. Tasks >100K tokens route to Gemini Flash's 1M context window.
5. **Embed locally:** Use `nomic-embed-text` [FUTURE] via Ollama for all embeddings. Never pay for external embedding APIs.
6. **Escalation Trigger:** A task is only escalated to Claude if Ollama's confidence score evaluates to < 0.75, or if the job envelope explicitly flags it as "final" or "client-facing".

***

## Section 3: n8n Trigger Types, Job Envelope Schema & Handoff Patterns

### Trigger Inventory

| Trigger Type | n8n Node | Use Case |
|---|---|---|
| File system watch | Local File Trigger | New media drop in ingest folders, Perplexity queue files in `%SFV_ROOT%\99_INBOX\QUEUE`, Obsidian vault writes |
| Scheduled cron | Schedule Trigger | Nightly vault sync, daily Sentinel health report, periodic embedding refresh |
| HTTP webhook | Webhook | Antigravity task dispatch, Python script callbacks, cross-node alerts |
| Manual | Manual Trigger | Testing, one-off jobs, development runs |
| n8n internal | Execute Workflow | Sub-workflow calls from orchestrator workflow |

### Standard Job Envelope Schema

All JSON payloads passing through the router or residing in `%SFV_ROOT%\99_INBOX\QUEUE` must adhere to this schema:

```json
{
  "task_id": "YYYYMMDD-###",
  "task_type": "CLASSIFY | SUMMARIZE | COMPRESS | RESEARCH | BLUEPRINT | CODE | MEDIA",
  "topic": "String",
  "prompt": "String",
  "priority": "NORMAL | HIGH | CRITICAL",
  "status": "PENDING | IN_PROGRESS | COMPLETE | ESCALATED | DEFERRED",
  "output_target": "%SFV_ROOT%\\99_INBOX\\OUTPUTS\\[filename]",
  "file_path": "Absolute path (if local file trigger)",
  "vault": "%SFV_ROOT%"
}
```

### Handoff Patterns

#### Pattern A: File-Based Handoff (Primary)
All tools communicate via structured files on disk. No agent edits canon directly without human approval.
```text
Producer writes: %SFV_ROOT%\99_INBOX\QUEUE\{timestamp}_{job_type}.json
n8n polls via File Trigger: detects new file → ingests → routes
Consumer writes: %SFV_ROOT%\99_INBOX\OUTPUTS\{output}.md
Antigravity or Claude reads output path, evaluates, logs to DECISION_LOG.md
```

#### Pattern B: Webhook Handoff (Real-Time)
For low-latency tasks where Antigravity needs a synchronous response.
```text
Antigravity POST → n8n webhook (sync, waits for response)
n8n executes → returns { status, output, artifact_path }
Antigravity receives result directly without polling
```

#### Pattern C: Ollama Direct (Bypass n8n for Speed)
Python scripts call Ollama directly for simple inference without routing overhead. Useful for sub-100ms routing latency.
```python
# Direct Ollama call
import httpx
response = httpx.post("http://[NodeB]:11434/api/generate",
    json={"model": "qwen3:14b", "prompt": prompt, "stream": False})
```

***

## Section 4: Sentinel Role (Node B)

The **Sentinel** resides on Node B (R&D Terminal - RTX 3060). Its role is 24/7 observation, local inference offloading, and Engine Body health monitoring.

**What it monitors:**
- Node A services availability (n8n port 5678, webhooks).
- GPU utilization and queuing bottlenecks.
- Ollama daemon response status.

**Alerting:**
If Node A services fail to respond, the Sentinel logs an alert locally and attempts to notify Will via defined fallback channels or dashboard indicators.

***

## Section 5: Gaps and Mitigations

The following critical Single Points of Failure (SPOFs) and structural gaps exist and are actively mitigated:

| Component | Failure Mode | Impact | Mitigation |
|---|---|---|---|
| n8n process crash | All routing stops | **Critical** | Sentinel restarts via Windows Service wrapper / `net start`. Queue mode (Redis) [FUTURE] prevents UI blocking. |
| Node B offline | Ollama unavailable | **High** | Node A Ollama acts as hot fallback; n8n IF node checks Node B health before routing. |
| Gemini Free Tier rate limit | Cloud burst lane saturates | **Medium** | Retry queue in n8n with exponential backoff; Ollama fallback for non-critical jobs. |
| Claude API outage | Premium outputs blocked | **Low** | Queue to file, retry on schedule; Gemini Flash as degraded fallback. |
| Vault Path Missing | Outputs fail silently | **Medium** | Use `%SFV_ROOT%` consistently. n8n error handlers write to `%SFV_ROOT%\99_INBOX\OUTPUTS\failed_jobs\` instead. |
| Concurrent Whisper runs | OOM memory crash | **High** | Implement serial media queue; utilize `faster-whisper` [FUTURE] to reduce memory footprint. |

***

## Section 6: Recommended Add-Ons [FUTURE]

> **STATUS:** [FUTURE]
> These add-ons are approved by Will, but remain labeled [FUTURE] until explicitly installed and integrated into the active running Engine.

1. **Redis [FUTURE]:** Job queue broker for n8n. Separates editor process from execution workers, preventing heavy media jobs from blocking Antigravity webhooks.
2. **Qdrant [FUTURE]:** Production-grade, Rust-based vector memory layer running locally on Node A. Resolves the gap of missing semantic retrieval and cross-session memory.
3. **`nomic-embed-text` [FUTURE]:** Local embedding model running via Ollama. Replaces expensive API embeddings and directly feeds Qdrant.
4. **`faster-whisper` [FUTURE]:** Python Flask backend replacing standard OpenAI Whisper. Dramatically reduces memory usage and speeds up transcription to prevent parallel OOM crashes.
5. **Prometheus + Grafana [FUTURE]:** Sentinel monitoring stack deployed on Node B. Scrapes n8n metrics to provide real-time observability over queue depth and execution failures.
6. **n8n-MCP [FUTURE]:** Model Context Protocol server. Exposes n8n workflow states and execution hooks directly to Claude and Antigravity, allowing natural language introspection of n8n.

***

> **FOR HUMAN REVIEW:**
> - Routing escalation threshold (Confidence < 0.75) — APPROVED by Will 2026-05-26. Keep as-is.
> - Ollama primary node — UNCONFIRMED. Resolve after Tailscale is live and latency is measured. Decision rules documented in Section 1.
