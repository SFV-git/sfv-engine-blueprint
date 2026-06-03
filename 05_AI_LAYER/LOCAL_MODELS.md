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

## ELECTRICITY MANAGEMENT [FOR HUMAN REVIEW]
R&D terminal should throttle when no active tasks.
Ollama has idle mode.
Estimated 40-60% power reduction during idle periods.
Full load only during active processing.

## CONNECTION TO ENGINE [UNCONFIRMED]
Tailscale recommended for secure private network between nodes.
R&D terminal pushes results to shared folder Engine monitors.
Will reviews proposals before Engine acts on them.

## INSTALL STEPS
```
1. ollama.ai → download for Windows
2. ollama pull qwen3
3. ollama pull llama3.1
4. (optional) install Open WebUI for browser interface
```

## CONNECTED FILES
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[METADATA_SYSTEM|Metadata System]]
- [[OLLAMA_SETUP|Ollama Setup]]
- [[STORAGE_ARCHITECTURE|Storage Architecture]]
- [[USAGE_OPTIMIZATION|Usage Optimization]]
