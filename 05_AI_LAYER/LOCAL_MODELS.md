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

## MODELS [UNCONFIRMED — install and test before locking]
- Qwen3: primary local model (strong reasoning, efficient)
- DeepSeek: coding and analysis tasks
- Llama 3.1: general purpose fallback
- Whisper: transcription (separate from Ollama)

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
- [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
- [[05_AI_LAYER/RATE_LIMITS|Rate Limits]]
- [[COMPRESSED_CONTEXT|Compressed Context]]
