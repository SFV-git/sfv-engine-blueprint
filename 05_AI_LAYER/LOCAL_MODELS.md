---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# LOCAL MODELS — R&D TERMINAL

## PURPOSE
Run AI tasks locally on R&D terminal at zero API cost.
Handle repetitive, low-complexity tasks 24/7.

## SETUP
- Tool: Ollama
- Interface: Open WebUI (optional)
- Machine: R&D Terminal (RTX 3060 / 16GB RAM)

## MODELS — R&D TERMINAL
- qwen3:8b — primary: classify, summarize, route (~5.2GB VRAM)
- qwen3:14b — secondary: code, complex reasoning (~10GB VRAM Q4_K_M)
- NEVER load both simultaneously. RTX 3060 = 12GB VRAM.
- OLLAMA_NUM_PARALLEL=1 required on R&D Terminal
- OLLAMA_KEEP_ALIVE=2m on R&D Terminal (short — avoids stale model hogging VRAM)

## TASKS HANDLED LOCALLY
- Blur detection
- Exposure flagging
- Duplicate grouping
- Metadata tagging
- Transcript generation (Whisper)
- Script matching
- Take ranking (lightweight version)
- Trend research synthesis
- Blueprint auditing

## ELECTRICITY MANAGEMENT (APPROVED 2026-05-27 — Proposal 004)
R&D terminal idles by default. Will gives heads-up before a shoot.
Ollama has idle mode.
Estimated 40-60% power reduction during idle periods.
Full load only during active processing.

## CONNECTION TO ENGINE (CONFIRMED 2026-05-27/28)
Direct ethernet ICS link (192.168.137.x) + Tailscale for remote access. Syncthing handles vault sync.
R&D Terminal reaches Engine Body Ollama at http://192.168.137.1:11434.
R&D terminal pushes results to shared folder Engine monitors.
Will reviews proposals before Engine acts on them.

## INSTALL STEPS (post-Win11 rebuild — Ollama needs reinstall on R&D Terminal)
```
1. ollama.ai → download for Windows
2. ollama pull qwen3:8b
3. ollama pull qwen3:14b
4. setx OLLAMA_NUM_PARALLEL 1 /M
5. setx OLLAMA_KEEP_ALIVE 2m /M
6. (optional) install Open WebUI for browser interface
```

## CONNECTED FILES
- [[VRAM_SCHEDULING_RULE|VRAM Scheduling Rule]]
- [[MODEL_ROUTING|Model Routing]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[USAGE_OPTIMIZATION|Usage Optimization]]
