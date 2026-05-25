---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-25
---

# R&D TERMINAL ARCHITECTURE — THE SENTINEL NODE

## PURPOSE
To offload observation, telemetry tracking, external web services, and sandboxed automations from the main Engine Body to the R&D Terminal (RTX 3060 / 16GB RAM).

This ensures the Engine Body (RTX 5080 / Ryzen 9) remains dedicated 100% to high-throughput media processing, system execution, and storage management without wasting cycles or exposing core systems to the public internet.

---

## CORE RESPONSIBILITIES

```mermaid
graph TD
    subgraph Engine Body [Engine Body (Worker)]
        A[Ingest Pipeline] -->|Write Logs| L[(Telemetry Logs)]
        B[Lightroom/Premiere] -->|Write Logs| L
        C[Media Processing] -->|Telemetry| L
    end

    subgraph RD Terminal [R&D Terminal (Observer & Gateway)]
        L -->|Sync via Tailscale| D[Telemetry Reader]
        D -->|Visualize| E[UI Overview Dashboard]
        F[Client Review Server] <-->|Secure Proxy| E
        G[Sandbox Agent] -->|Polymarket / Alpaca APIs| H[Algorithmic Trading]
    end

    subgraph Client [External Web]
        I[Client View] <--> F
    end
```

### 1. Telemetry & UI Overview
The R&D Terminal hosts a local web dashboard that parses system activity from both machines.
- **Workflow Monitoring**: Visual tracking of ingestion times, culling durations, render queues, and exports.
- **System Health**: CPU/GPU temperature, RAM utilization, and disk read/write throughput to detect hardware throttles (e.g., thermal limiters or slow cable bottlenecks).
- **Dashboard Stack**: Streamlit or React dashboard reading from unified JSON log streams.

### 2. Client Review Gateway (Reels & Photo Review)
To prevent security leaks or service exhaustion attacks on the primary Engine Body, the public-facing review system is served from the R&D Terminal.
- **Network Isolation**: The Engine Body never accepts incoming connections from the public web.
- **Cached Asset Serving**: Client review pages (selects, drafts, reels) are served via the R&D Terminal. It caches files requested from the Engine Body over Tailscale.

### 3. Workflow Optimization Engine
An offline, local LLM (Qwen/DeepSeek) runs periodically to analyze log history and suggest efficiency modifications.
- **Bottleneck Detection**: "Ingest speeds on Fielding drive dropped 30% below baseline. Recommendation: Run file system health check on SanDisk SSD."
- **Queue Balancing**: Alerts when background processes on the Engine Body are overlapping inefficiently.

### 4. Sandbox Investing Node
A sandboxed container running automated trading scripts using a set allocation of capital.
- **Isolation**: Stored keys (Polymarket, Alpaca, or Interactive Brokers APIs) and executing code are isolated inside a Docker container on the R&D Terminal.
- **Scope**: Run experimental algorithmic trading strategies with $200–$300 budget. Zero risk to Engine data.

---

## INFRASTRUCTURE REQUIREMENTS

- **Tailscale**: Setup encrypted private network between both machines.
- **File Syncing**: Share `/telemetry_logs` and `/client_preview_cache` folders securely.
- **Docker**: Run the sandbox investing node and client review server in containerized environments.

---

## NEXT ACTIONS

1. **Phase 1 (Current)**: Setup basic logs folder and track pipeline steps.
2. **Phase 2 (Telemetry)**: Write log output scripts for Ingest/Export steps.
3. **Phase 3 (Gateway)**: Build lightweight client review interface.
4. **Phase 4 (Sandbox)**: Initialize sandbox investing python environment.
