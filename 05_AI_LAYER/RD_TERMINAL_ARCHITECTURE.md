---
STATUS: CANON
VERSION: v0.2.0
OWNER: WILL
LAST_UPDATED: 2026-05-27
APPROVED: 2026-05-26 — Proposal 007 confirmed by Will
---

# R&D TERMINAL ARCHITECTURE — THE SENTINEL

## CONCEPT
Evolve the R&D Terminal from a local model serving box into a full Sentinel node.
Four distinct roles, all isolated from the Engine Body (the worker).
Engine Body stays heads-down on production. R&D Terminal watches, serves, and experiments.

## CONNECTED FILES
- [[05_AI_LAYER/LOCAL_MODELS|Local Models]]
- [[03_INFRASTRUCTURE/STORAGE_ARCHITECTURE|Storage Architecture]]
- [[03_INFRASTRUCTURE/ENVIRONMENT_CONFIG|Environment Config]]
- [[FOR_HUMAN_REVIEW/PROPOSALS|Proposals]]
- [[COMPRESSED_CONTEXT|Compressed Context]]

---

## HARDWARE BASELINE (R&D TERMINAL)
- GPU: RTX 3060 (12GB VRAM)
- RAM: 16GB
- Availability: 24/7
- Network: Same LAN as Engine Body + Tailscale (if approved)

---

## ROLE 1 — TELEMETRY READER + WORKFLOW DASHBOARD

### Problem
Running monitoring dashboards on the Engine Body wastes processing cycles
that should be on ingest, rendering, and Lightroom.

### Setup
Engine Body writes lightweight JSON telemetry logs per workflow step:
```json
{
  "workflow": "ingest",
  "branch": "SFV_STUDIO",
  "files": 152,
  "duration_s": 343,
  "gpu_temp_c": 72,
  "disk_write_mbps": 180,
  "errors": 0,
  "timestamp": "2026-05-28T14:32:01"
}
```
Logs land in: `D:\SFV_ACTIVE\LOGS\TELEMETRY\`
R&D Terminal reads these logs over Tailscale (or shared network path).

### R&D Terminal Role
- Runs a lightweight Streamlit or React dashboard
- Plots: throughput, bottlenecks, GPU temp, disk speed, error rates
- Surfaces: "ingest took 43% longer than baseline — E:\ is the bottleneck"
- Accessible at: http://[rnd-terminal-ip]:8501 from any device on local network

### Dependencies
- Tailscale (Proposal 002) — for secure log sync
- Python + Streamlit OR lightweight React build
- No GPU required — pure CPU dashboard task

---

## ROLE 2 — CLIENT REVIEW GATEWAY (SECURE PROXY)

### Problem
Giving clients direct access to Engine Body exposes:
- Raw files and financial data
- System control APIs
- All active storage on D:\

### Setup
R&D Terminal acts as a reverse proxy / caching server.
Clients access the R&D Terminal, never the Engine Body.

```
Client browser → R&D Terminal (reverse proxy + cache)
                    ↓ (Tailscale, internal only)
               Engine Body (pulls review assets on request)
```

### R&D Terminal Role
- Hosts the client-facing web app (reel review, photo selection)
- Queries Engine Body over Tailscale for review assets only
- Caches assets locally so Engine Body isn't hit repeatedly
- If review server is compromised: Engine Body is completely unaffected

### Delivers
- Clients review reels and selects from a clean web interface
- No Pixieset dependency for internal review (Pixieset still used for delivery)
- Engine Body stays air-gapped from the internet

### Dependencies
- Tailscale (Proposal 002) — required
- nginx or Caddy as reverse proxy (lightweight)
- Simple React or Next.js client review app
- Docker recommended for isolation (Proposal — Docker status: UNCONFIRMED)

---

## ROLE 3 — WORKFLOW OPTIMIZATION ENGINE (LOCAL AGENT)

### Setup
A local agent (Qwen3 on Ollama — already running) continuously reviews telemetry logs.
This is an extension of the existing Ollama daemon, not a new system.

### R&D Terminal Role
Detects patterns in telemetry and surfaces optimization prompts:

Examples:
- "UGC culling is taking 40% longer on Mondays. Recommendation: pre-stage culling folders Sunday night."
- "ingest.py copy step averages 8 min for 150 files. Bottleneck: E:\ read speed. Recommendation: test with USB 3.2 hub."
- "SFV_STUDIO exports cluster between 2-4pm. GPU temp spikes to 85C. Recommendation: schedule exports for off-peak."

### How it runs
Add to TASK_QUEUE.md (already working):
```
READ: D:\SFV_ACTIVE\LOGS\TELEMETRY\latest.json
Analyze this telemetry log. Identify one workflow bottleneck.
Output: one specific, actionable recommendation. No preamble.
```

### Dependencies
- Ollama daemon (already running) — just needs telemetry log access
- Telemetry JSON format (needs ingest.py + future scripts to emit logs)
- No new tools required

---

## ROLE 4 — SANDBOX INVESTOR (TRADING ISOLATION)

### Problem
- Financial trading APIs require 24/7 uptime and expose API keys
- A bug in a trading script should NEVER be able to touch production storage
- Testing experimental models needs an isolated environment

### Setup
Completely isolated Docker container on R&D Terminal.
Engine Body has zero knowledge this exists.

```
Docker container (R&D Terminal only):
├── Python trading script
├── Polymarket API client
├── Alpaca API client (stocks)
├── Budget: $200-300 CAD set budget, hard stop
└── Logs: written to container only, not to vault
```

### R&D Terminal Role
- Container starts/stops independently
- If the script goes wrong: container destroyed, $[budget] lost, Engine Body untouched
- Budget enforcement: Alpaca + Polymarket both support max position limits

### Risk profile
- Maximum loss: set budget ($200-300)
- Engine Body exposure: zero
- Vault exposure: zero
- Recovery: rebuild container from scratch

### Dependencies
- Docker (Proposal — status: UNCONFIRMED — decision needed)
- Polymarket API access
- Alpaca API access (free tier available)
- Set budget before activating — Will controls this number

---

## IMPLEMENTATION ORDER (if approved)

| Phase | What | Requires |
|-------|------|----------|
| 1 | Telemetry JSON output from ingest.py | ingest.py already built |
| 2 | Streamlit dashboard on R&D Terminal | pip install streamlit |
| 3 | Tailscale setup (Proposal 002) | Will approval |
| 4 | Client Review Gateway | Tailscale + nginx |
| 5 | Optimization agent (Ollama) | Telemetry logs flowing |
| 6 | Trading sandbox | Docker approval + budget decision |

---

## WHAT NEEDS WILL'S DECISION

1. **Approve Proposal 007** in PROPOSALS.md → unlocks Phase 1
2. **Approve Tailscale** (Proposal 002) → unlocks Phases 3-5
3. **Approve Docker** → unlocks Phase 6
4. **Set trading budget** → required before Phase 6 activates

---
*Architecture proposed by Antigravity 2026-05-25.*
*Engine Body stays isolated. R&D Terminal becomes the observer.*
